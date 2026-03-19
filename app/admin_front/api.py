from __future__ import annotations

import re
import uuid
from typing import Any
from urllib.parse import quote

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_front.deps import PanelAdminUser
from app.admin_front.registry import (
    SECTIONS,
    get_resource_definition,
    list_resource_descriptors,
    IMAGE_ACCEPT,
)
from app.admin_front.schemas import (
    ActionExecuteIn,
    ActionExecuteOut,
    BootstrapPayload,
    DashboardSummary,
    OptionItem,
    UploadResponse,
)
from app.core.config import settings
from app.db.engine import get_session
from app.db.models.country import Country
from app.db.models.hotel import Hotel
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.utils.s3 import minio_client


router = APIRouter(prefix="/panel-api", tags=["admin-front"])


def _public_media_url(object_key: str) -> str:
    return f"{settings.s3.url}/{object_key}"


def _safe_filename(name: str) -> str:
    stripped = name.strip().replace(" ", "-").lower()
    return "".join(ch for ch in stripped if ch.isalnum() or ch in {"-", "_", "."}) or "file"


def _object_prefix(entity: str) -> str:
    mapping = {
        "country": "countries",
        "route": "routes",
        "hotel": "hotels",
        "restaurant": "restaurants",
        "icon": "icons",
    }
    return mapping.get(entity, "uploads")


def _build_action_catalog(openapi_schema: dict[str, Any]) -> dict[str, Any]:
    filtered_paths: dict[str, Any] = {}
    for path, operations in openapi_schema.get("paths", {}).items():
        if not path.startswith("/api/v1"):
            continue
        filtered_ops: dict[str, Any] = {}
        for method, details in operations.items():
            if method.lower() not in {"get", "post", "patch", "put", "delete"}:
                continue
            filtered_ops[method] = {
                "summary": details.get("summary"),
                "description": details.get("description"),
                "tags": details.get("tags", []),
                "parameters": details.get("parameters", []),
                "requestBody": details.get("requestBody"),
                "security": details.get("security", []),
            }
        if filtered_ops:
            filtered_paths[path] = filtered_ops
    return {
        "paths": filtered_paths,
        "components": {"schemas": openapi_schema.get("components", {}).get("schemas", {})},
    }


def _interpolate_path(path_template: str, path_params: dict[str, Any]) -> str:
    result = path_template
    for key, value in path_params.items():
        result = result.replace(f"{{{key}}}", quote(str(value), safe=""))
    if re.search(r"{[^}]+}", result):
        raise HTTPException(status_code=400, detail="Не заполнены path-параметры.")
    return result


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard(
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> DashboardSummary:
    countries = await session.scalar(select(func.count(Country.id))) or 0
    routes = await session.scalar(select(func.count(Route.id))) or 0
    hotels = await session.scalar(select(func.count(Hotel.id))) or 0
    restaurants = await session.scalar(select(func.count(Restaurant.id))) or 0
    return DashboardSummary(
        countries=countries,
        routes=routes,
        hotels=hotels,
        restaurants=restaurants,
    )


@router.get("/meta/bootstrap", response_model=BootstrapPayload)
async def get_bootstrap_meta(request: Request, user: PanelAdminUser) -> BootstrapPayload:
    from app.admin_front.auth import _panel_user

    return BootstrapPayload(
        user=_panel_user(user),
        sections=SECTIONS,
        resources=list_resource_descriptors(),
        actions=_build_action_catalog(request.app.openapi()),
    )


@router.get("/resources/{resource_id}/items")
async def list_resource_items(
    resource_id: str,
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    definition = get_resource_definition(resource_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Ресурс не найден.")
    return await definition.list_loader(session)


@router.get("/resources/{resource_id}/options", response_model=list[OptionItem])
async def get_resource_options(
    resource_id: str,
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> list[OptionItem]:
    definition = get_resource_definition(resource_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Ресурс не найден.")
    if not definition.options_loader:
        return []
    return await definition.options_loader(session)


@router.post("/resources/{resource_id}/items")
async def create_resource_item(
    resource_id: str,
    payload: dict[str, Any],
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    definition = get_resource_definition(resource_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Ресурс не найден.")
    validated = definition.payload_model.model_validate(payload)
    return await definition.create_handler(session, validated)


@router.patch("/resources/{resource_id}/items/{item_id}")
async def update_resource_item(
    resource_id: str,
    item_id: uuid.UUID,
    payload: dict[str, Any],
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    definition = get_resource_definition(resource_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Ресурс не найден.")
    validated = definition.payload_model.model_validate(payload)
    try:
        return await definition.update_handler(session, item_id, validated)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/resources/{resource_id}/items/{item_id}")
async def delete_resource_item(
    resource_id: str,
    item_id: uuid.UUID,
    user: PanelAdminUser,
    session: AsyncSession = Depends(get_session),
) -> dict[str, bool]:
    definition = get_resource_definition(resource_id)
    if not definition:
        raise HTTPException(status_code=404, detail="Ресурс не найден.")
    try:
        await definition.delete_handler(session, item_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"ok": True}


@router.post("/actions/execute", response_model=ActionExecuteOut)
async def execute_api_action(
    payload: ActionExecuteIn,
    request: Request,
    user: PanelAdminUser,
) -> ActionExecuteOut:
    path = _interpolate_path(payload.path, payload.path_params)
    headers = {key: value for key, value in payload.headers.items() if value}
    if payload.use_current_auth and request.headers.get("authorization"):
        headers.setdefault("authorization", request.headers["authorization"])

    params = {key: value for key, value in payload.query_params.items() if value not in ("", None)}
    json_body = payload.json_body if payload.method.upper() in {"POST", "PATCH", "PUT", "DELETE"} else None

    transport = httpx.ASGITransport(app=request.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://panel.local") as client:
        response = await client.request(
            payload.method.upper(),
            path,
            params=params,
            json=json_body,
            headers=headers,
        )

    try:
        body = response.json()
        is_json = True
    except ValueError:
        body = response.text
        is_json = False

    return ActionExecuteOut(
        statusCode=response.status_code,
        headers={
            key: value
            for key, value in response.headers.items()
            if key.lower() in {"content-type", "location"}
        },
        body=body,
        isJson=is_json,
    )


@router.post("/uploads/{entity_type}", response_model=UploadResponse)
@router.post("/upload/{entity_type}", response_model=UploadResponse, include_in_schema=False)
async def upload_media(
    entity_type: str,
    user: PanelAdminUser,
    file: UploadFile = File(...),
) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Пустое имя файла.")
    if file.content_type not in IMAGE_ACCEPT:
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла.")

    object_key = f"{_object_prefix(entity_type)}/{uuid.uuid4().hex}-{_safe_filename(file.filename)}"
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Пустой файл.")

    try:
        uploaded_key = await minio_client.upload_file(content, object_key)
    except Exception as exc:
        message = str(exc)
        if "413" in message or "Request Entity Too Large" in message:
            raise HTTPException(
                status_code=413,
                detail="Файл слишком большой для загрузки в S3. Уменьши изображение или увеличь client_max_body_size на nginx для s3-media.",
            ) from exc
        raise HTTPException(
            status_code=502,
            detail=f"Ошибка загрузки в S3: {message}",
        ) from exc

    return UploadResponse(
        object_key=uploaded_key,
        public_url=_public_media_url(uploaded_key),
    )
