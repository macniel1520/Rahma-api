from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app.admin_front.api import router as panel_api_router
from app.admin_front.auth import router as panel_auth_router


BASE_DIR = Path(__file__).resolve().parents[2]
ADMIN_FRONT_DIR = BASE_DIR / "admin-front"
ADMIN_DIST_DIR = ADMIN_FRONT_DIR / "dist"


def setup_admin_front(app: FastAPI) -> None:
    app.include_router(panel_auth_router)
    app.include_router(panel_api_router)

    if ADMIN_DIST_DIR.exists():
        app.mount("/panel-assets", StaticFiles(directory=ADMIN_DIST_DIR), name="panel-assets")

    def serve_panel_index():
        index_file = ADMIN_DIST_DIR / "index.html"
        if not index_file.exists():
            return PlainTextResponse(
                "Новая админка ещё не собрана. Пересобери контейнер или выполни фронтенд build.",
                status_code=503,
            )
        return FileResponse(index_file)

    @app.get("/panel", include_in_schema=False)
    @app.get("/panel/{path:path}", include_in_schema=False)
    async def panel_index(path: str = ""):
        return serve_panel_index()
