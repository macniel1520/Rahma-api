from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.amal.amal_category_schema import AmalCategoryRead
from app.api.v1.schemas.amal.icon_schema import IconRead
from app.db.cruds.amal_category_repository import SqlAlchemyAmalCategoryRepository
from app.db.cruds.icon_repository import SqlAlchemyIconRepository
from app.db.engine import get_session
from app.services.amal.reference_service import ReferenceService

router = APIRouter(prefix="/reference", tags=["reference"])


def get_reference_service(session: AsyncSession = Depends(get_session)) -> ReferenceService:
    return ReferenceService(
        category_repo=SqlAlchemyAmalCategoryRepository(session=session),
        icon_repo=SqlAlchemyIconRepository(session=session),
    )


@router.get(
    "/categories",
    response_model=list[AmalCategoryRead],
    summary="Получить все категории амалов",
    description="Получение списка всех категорий амалов.",
    response_description="Список категорий амалов",
)
async def get_categories(
    service: ReferenceService = Depends(get_reference_service),
) -> list[AmalCategoryRead]:
    return await service.get_all_categories()


@router.get(
    "/icons",
    response_model=list[IconRead],
    summary="Получить все иконки",
    description="Получение списка всех иконок для амалов.",
    response_description="Список иконок",
)
async def get_icons(
    service: ReferenceService = Depends(get_reference_service),
) -> list[IconRead]:
    return await service.get_all_icons()
