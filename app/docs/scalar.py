from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

def setup_scalar(app: FastAPI) -> None:
    """Добавляет кастомный Scalar UI."""
    @app.get("/scalar", include_in_schema=False)
    async def scalar_ui():
        """Scalar API Reference UI."""
        return get_scalar_api_reference(
            openapi_url="/openapi.json",
            title=app.title
        )