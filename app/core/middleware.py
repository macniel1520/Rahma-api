from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.middlewares.correlation_id import CorrelationIdMiddleware
from app.api.middlewares.request_logging import RequestLoggingMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
    # Respect reverse-proxy X-Forwarded-* headers so generated admin URLs keep HTTPS.
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
