from fastapi import APIRouter, FastAPI

from app.api.v1.routers.country_router import router as country_router


def setup_routes(app: FastAPI) -> None:
    api_router = APIRouter(
        prefix="/api/v1",
    )
    ...  # TODO: Add routes
    app.include_router(api_router)
    app.include_router(country_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
