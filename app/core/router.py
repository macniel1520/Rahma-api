from fastapi import APIRouter, FastAPI

from app.api.v1.routers.user.auth import router as auth_router
from app.api.v1.routers.user.users import router as users_router


def setup_routes(app: FastAPI) -> None:
    api_router = APIRouter(
        prefix="/api/v1",
    )
    app.include_router(api_router)
    api_router.include_router(auth_router)
    api_router.include_router(users_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
