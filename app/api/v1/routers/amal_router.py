from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import exceptions
from app.api.v1.schemas.amal.amal_schema import AmalSyncRequest, AmalSyncResponse
from app.db.cruds.amal_completion_repository import SqlAlchemyAmalCompletionRepository
from app.db.cruds.amal_repository import SqlAlchemyAmalRepository
from app.db.engine import get_session
from app.services.amal.amal_service import AmalService
from app.services.auth.current_user import CurrentUser

router = APIRouter(prefix="/amals", tags=["amals"])


def get_amal_service(session: AsyncSession = Depends(get_session)) -> AmalService:
    return AmalService(
        amal_repo=SqlAlchemyAmalRepository(session=session),
        completion_repo=SqlAlchemyAmalCompletionRepository(session=session),
    )


@router.get(
    "/sync",
    response_model=AmalSyncResponse,
    summary="Получить все амалы",
    description="Получение всех амалов пользователя.",
    response_description="Список амалов пользователя",
)
async def get_amals(
    current_user: CurrentUser,
    service: AmalService = Depends(get_amal_service),
) -> AmalSyncResponse:
    return await service.get_all(user_id=current_user.id)


@router.post(
    "/sync",
    response_model=AmalSyncResponse,
    summary="Синхронизация амалов",
    description="Синхронизация амалов пользователя.",
    response_description="Амалы успешно синхронизированы",
)
async def sync_amals(
    request: AmalSyncRequest,
    current_user: CurrentUser,
    service: AmalService = Depends(get_amal_service),
) -> AmalSyncResponse:
    try:
        return await service.sync(user_id=current_user.id, request=request)
    except IntegrityError as e:
        if "ForeignKeyViolationError" in str(e):
            raise exceptions.foreign_key_not_found_exc()
        raise
