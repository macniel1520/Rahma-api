from fastapi import APIRouter, Depends

from app.api.v1.schemas.jes.jes import JesAuthResponse
from app.services.jes.jes import (
    JesService,
    JesTimeoutError,
    JesNetworkError,
    JesUpstreamError,
)
from app.api.v1.exceptions import jes_timeout_exc, jes_network_exc, jes_upstream_exc
from app.docs.responses import (
    jes_timeout_response,
    jes_network_response,
    jes_upstream_response,
)
from app.services.auth.current_user import CurrentUser

router = APIRouter(prefix="/jes", tags=["jes"])


def get_jes_service() -> JesService:
    return JesService()


@router.get(
    "/authtoken/user",
    summary="Получить Url для JES esim",
    description="Получение реферальной ссылки для JES esim",
    response_description="Реферальная ссылка для JES esim",
    responses={**jes_timeout_response, **jes_network_response, **jes_upstream_response},
)
async def authtoken_user(
    current_user: CurrentUser,
    service: JesService = Depends(get_jes_service),
) -> JesAuthResponse:
    try:
        return await service.create_user_token(email=current_user.email)
    except JesTimeoutError:
        raise jes_timeout_exc()
    except JesNetworkError:
        raise jes_network_exc()
    except JesUpstreamError:
        raise jes_upstream_exc()
