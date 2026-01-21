import time
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.structlog_config import logger

log = logger.bind(module=__name__, service="rahma-api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Logs every HTTP request.

        Logging details:
          - Logs 'request.started' with method, path, client IP, and query parameters at the start of each request.
          - Logs 'request.finished' with status code and processing time upon completion.
          - Logs 'request.failed' with stack trace and error details if an unhandled exception occurs.

        The 'correlation_id' field will be automatically loaded from contextvars,
        as set by CorrelationIdMiddleware.
        """
        start_time = time.perf_counter()
        correlation_id = getattr(request.state, "correlation_id", None)

        log.info(
            "request.started",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query) if request.url.query else "",
            client_ip=request.client.host if request.client else None,
            correlation_id=correlation_id,
        )

        try:
            response: Response = await call_next(request)
        except Exception as e:
            process_time = time.perf_counter() - start_time
            log.exception(
                "request.failed",
                method=request.method,
                path=request.url.path,
                process_time_ms=int(process_time * 1000),
                correlation_id=correlation_id,
                error=str(e),
            )
            raise

        process_time = time.perf_counter() - start_time

        log.info(
            "request.finished",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=int(process_time * 1000),
            correlation_id=correlation_id,
        )

        return response
