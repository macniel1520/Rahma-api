from app.utils.structlog_config import setup_logging
from app.core.middleware import setup_middlewares
from app.core.router import setup_routes
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="SRL Wrapper API",
        version="1.0.0",
    )

    setup_logging()
    setup_middlewares(app)
    setup_routes(app)

    return app


app = create_app()
