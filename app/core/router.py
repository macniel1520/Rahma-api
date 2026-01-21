
from fastapi import APIRouter, FastAPI


def setup_routes(app: FastAPI) -> None:
    api_router = APIRouter(
        prefix="/api/v1",
    )
    ... # TODO: Add routes
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
