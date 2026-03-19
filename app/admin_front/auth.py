from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_front.deps import PanelAdminUser
from app.admin_front.schemas import PanelAuthResponse, PanelUser
from app.api.v1.schemas.auth.session import LoginIn, LogoutIn, RefreshIn
from app.db.cruds.users import get_by_email, get_by_id
from app.db.engine import get_session
from app.db.models.user import User
from app.services.auth.auth_service import InvalidCredentials, login_with_email_password
from app.services.auth.tokens import (
    InvalidRefresh,
    decode_access_token,
    decode_refresh_token,
    revoke_refresh,
    rotate_refresh,
)


router = APIRouter(prefix="/panel-api/auth", tags=["admin-front-auth"])


def _panel_user(user: User) -> PanelUser:
    return PanelUser(
        id=user.id,
        email=user.email,
        name=user.name or user.email,
        isSuperuser=user.is_superuser,
    )


@router.post("/login", response_model=PanelAuthResponse)
async def panel_login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
) -> PanelAuthResponse:
    user = await get_by_email(session, str(data.email))
    if not user or not user.is_superuser or not user.is_active or not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные данные для входа в админку.",
        )

    try:
        tokens = await login_with_email_password(
            session=session,
            email=str(data.email),
            password=data.password,
        )
    except InvalidCredentials as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные данные для входа в админку.",
        ) from exc

    return PanelAuthResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=_panel_user(user),
    )


@router.post("/refresh", response_model=PanelAuthResponse)
async def panel_refresh(
    data: RefreshIn,
    session: AsyncSession = Depends(get_session),
) -> PanelAuthResponse:
    try:
        refresh_payload = decode_refresh_token(data.refresh_token)
        user_id = UUID(refresh_payload["sub"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен обновления недействителен.",
        ) from exc

    user = await get_by_id(session, user_id)
    if not user or not user.is_superuser or not user.is_active or not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ к админке запрещён.",
        )

    try:
        tokens = await rotate_refresh(session, refresh_token=data.refresh_token)
        access_payload = decode_access_token(tokens.access_token)
        access_user = await get_by_id(session, UUID(access_payload["sub"]))
    except InvalidRefresh as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен обновления недействителен.",
        ) from exc

    if not access_user or not access_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ к админке запрещён.",
        )

    return PanelAuthResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=_panel_user(access_user),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def panel_logout(
    data: LogoutIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    await revoke_refresh(session=session, refresh_token=data.refresh_token)
    return None


@router.get("/me", response_model=PanelUser)
async def panel_me(user: PanelAdminUser) -> PanelUser:
    return _panel_user(user)
