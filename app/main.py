from fastapi import FastAPI

from app.admin.admin import create_admin_app
from app.core.error import register_exception_handlers
from app.core.middleware import setup_middlewares
from app.core.router import setup_routes
from app.docs.elements import setup_elements
from app.docs.openapi import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    SERVERS,
    TAGS_METADATA,
)
from app.docs.scalar import setup_scalar
from app.utils.structlog_config import setup_logging


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        openapi_tags=TAGS_METADATA,
        docs_url="/docs",
        redoc_url="/redoc",
        servers=SERVERS,
        separate_input_output_schemas=True,
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
            "docExpansion": "none",
            "defaultModelsExpandDepth": 2,
            "defaultModelExpandDepth": 2,
            "deepLinking": True,
            "syntaxHighlight": {"theme": "obsidian"},
        },
        generate_unique_id_function=lambda route: route.name,
    )

    setup_logging()
    setup_middlewares(app)
    register_exception_handlers(app)
    setup_routes(app)
    setup_scalar(app)
    setup_elements(app)
    create_admin_app(app)

    return app


app = create_app()
