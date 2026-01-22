from fastapi import FastAPI

from app.core.middleware import setup_middlewares
from app.core.router import setup_routes
from app.utils.structlog_config import setup_logging
from app.docs.scalar import setup_scalar


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rahma API",
        version="1.0.0",
    )

    setup_logging()
    setup_middlewares(app)
    setup_routes(app)
    setup_scalar(app)

    return app


app = create_app()
