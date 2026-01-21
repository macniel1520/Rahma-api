import uuid
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

HEADER_NAME = "x-correlation-id"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Ensures that each incoming request has a `correlation_id`.

        If the request contains the `x-correlation-id` header, uses its value.
        Otherwise, generates a new UUIDv4. The correlation ID is set in
        `request.state.correlation_id`, added to structlog's contextvars for
        logging, and included in the response headers.

        Returns:
            None. (The correlation ID is set as described above.)
        """
        correlation_id = request.headers.get(HEADER_NAME) or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        bind_contextvars(correlation_id=correlation_id)

        try:
            response: Response = await call_next(request)
        finally:
            clear_contextvars()

        response.headers[HEADER_NAME] = correlation_id

        return response