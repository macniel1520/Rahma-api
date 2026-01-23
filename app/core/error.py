from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.utils.structlog_config import logger

log = logger.bind(module=__name__, service="rahma-api")


def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail

        error_code = None
        message = None
        meta = None

        if isinstance(detail, dict):
            error_code = detail.get("error")
            message = detail.get("message")
            meta = detail.get("meta")
        else:
            message = str(detail)

        log.warning(
            "request.http_exception",
            method=request.method,
            path=request.url.path,
            status_code=exc.status_code,
            error_code=error_code,
            message=message,
            meta=meta,
            detail=detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail},
        )
