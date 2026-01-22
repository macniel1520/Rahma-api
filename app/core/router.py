from fastapi import APIRouter, FastAPI

from app.api.v1.routers.amal_router import router as amal_router
from app.api.v1.routers.user.auth import router as auth_router
from app.api.v1.routers.user.users import router as users_router
from app.api.v1.routers.user.session import router as session_router
from app.api.v1.routers.country_router import router as country_router
from app.api.v1.routers.route_router import router as route_router


def setup_routes(app: FastAPI) -> None:
    api_router = APIRouter(
        prefix="/api/v1",
    )
    api_router.include_router(amal_router)
    api_router.include_router(auth_router)
    api_router.include_router(users_router)
    api_router.include_router(session_router)
    api_router.include_router(country_router)
    api_router.include_router(route_router)
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
