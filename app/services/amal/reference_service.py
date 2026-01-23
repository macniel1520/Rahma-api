from app.api.v1.schemas.amal.amal_category_schema import AmalCategoryRead
from app.api.v1.schemas.amal.icon_schema import IconRead
from app.db.cruds.amal_category_repository import AmalCategoryRepository
from app.db.cruds.icon_repository import IconRepository


class ReferenceService:
    def __init__(
        self,
        category_repo: AmalCategoryRepository,
        icon_repo: IconRepository,
    ):
        self._category_repo = category_repo
        self._icon_repo = icon_repo

    async def get_all_categories(self) -> list[AmalCategoryRead]:
        categories = await self._category_repo.get_all()
        return [AmalCategoryRead.model_validate(cat) for cat in categories]

    async def get_all_icons(self) -> list[IconRead]:
        icons = await self._icon_repo.get_all()
        return [IconRead.model_validate(icon) for icon in icons]
