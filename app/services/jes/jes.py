from __future__ import annotations

from typing import Any

import httpx

from app.api.v1.schemas.jes.jes import JesAuthResponse
from app.core.config import settings


class JesServiceError(RuntimeError):
    """Базовая ошибка сервиса JES."""


class JesUpstreamError(JesServiceError):
    """JES вернул не-2xx или некорректный ответ."""


class JesTimeoutError(JesServiceError):
    """Таймаут при обращении к JES."""


class JesNetworkError(JesServiceError):
    """Сетевая ошибка при обращении к JES."""


class JesService:
    def __init__(self) -> None:
        self._config = settings.jes

    @property
    def _user_token_url(self) -> str:
        return f"{self._config.base_url}/wh/authtoken/user/"

    async def create_user_token(self, email: str) -> JesAuthResponse:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self._config.api_key,
        }

        timeout = httpx.Timeout(self._config.timeout_seconds, connect=5.0)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(
                    self._user_token_url,
                    json={"email": email},
                    headers=headers,
                )
        except httpx.TimeoutException as e:
            raise JesTimeoutError("Timeout while calling JES") from e
        except httpx.RequestError as e:
            raise JesNetworkError(f"Network error while calling JES: {e!s}") from e

        if resp.status_code < 200 or resp.status_code >= 300:
            raise JesUpstreamError(
                f"JES returned non-2xx status: {resp.status_code}. Body: {self._safe_body(resp)}"
            )

        data = self._safe_json(resp)
        try:
            return JesAuthResponse(**data)
        except Exception as e:
            raise JesUpstreamError(
                f"Unexpected JES response format. Body: {data}"
            ) from e

    @staticmethod
    def _safe_json(resp: httpx.Response) -> dict[str, Any]:
        try:
            return resp.json()
        except Exception:
            raise JesUpstreamError(f"JES response is not valid JSON. Body: {resp.text}")

    @staticmethod
    def _safe_body(resp: httpx.Response) -> Any:
        try:
            return resp.json()
        except Exception:
            return resp.text
