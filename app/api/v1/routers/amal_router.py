from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.amal.amal_schema import AmalSyncRequest, AmalSyncResponse
from app.db.cruds.amal_category_repository import SqlAlchemyAmalCategoryRepository
from app.db.cruds.amal_completion_repository import SqlAlchemyAmalCompletionRepository
from app.db.cruds.amal_repository import SqlAlchemyAmalRepository
from app.db.cruds.icon_repository import SqlAlchemyIconRepository
from app.db.engine import get_session
from app.services.amal.amal_service import AmalService
from app.services.auth.current_user import CurrentUser

router = APIRouter(prefix="/amal", tags=["amal"])


def get_amal_service(session: AsyncSession = Depends(get_session)) -> AmalService:
    return AmalService(
        amal_repo=SqlAlchemyAmalRepository(session=session),
        category_repo=SqlAlchemyAmalCategoryRepository(session=session),
        completion_repo=SqlAlchemyAmalCompletionRepository(session=session),
        icon_repo=SqlAlchemyIconRepository(session=session),
    )


@router.get("/sync", response_model=AmalSyncResponse)
async def get_amals(
    current_user: CurrentUser,
    service: AmalService = Depends(get_amal_service),
) -> AmalSyncResponse:
    return await service.get_all(user_id=current_user.id)


@router.post("/sync", response_model=AmalSyncResponse)
async def sync_amals(
    request: AmalSyncRequest,
    current_user: CurrentUser,
    service: AmalService = Depends(get_amal_service),
) -> AmalSyncResponse:
    return await service.sync(user_id=current_user.id, request=request)
