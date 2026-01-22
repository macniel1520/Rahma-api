from uuid import UUID

from app.api.v1.schemas.amal.amal_schema import (
    AmalCreate,
    AmalRead,
    AmalSyncRequest,
    AmalSyncResponse,
)
from app.api.v1.schemas.amal.amal_category_schema import AmalCategoryRead
from app.api.v1.schemas.amal.amal_completion_schema import (
    AmalCompletionCreate,
    AmalCompletionRead,
)
from app.api.v1.schemas.amal.icon_schema import IconRead
from app.db.cruds.amal_repository import AmalRepository
from app.db.cruds.amal_category_repository import AmalCategoryRepository
from app.db.cruds.amal_completion_repository import AmalCompletionRepository
from app.db.cruds.icon_repository import IconRepository


class AmalService:
    def __init__(
        self,
        amal_repo: AmalRepository,
        category_repo: AmalCategoryRepository,
        completion_repo: AmalCompletionRepository,
        icon_repo: IconRepository,
    ):
        self._amal_repo = amal_repo
        self._category_repo = category_repo
        self._completion_repo = completion_repo
        self._icon_repo = icon_repo

    async def sync(
        self,
        *,
        user_id: UUID,
        request: AmalSyncRequest,
    ) -> AmalSyncResponse:
        if request.amals:
            await self._amal_repo.upsert_many(
                amals=[self._amal_to_dict(amal, user_id) for amal in request.amals]
            )

        if request.deletedAmalIds:
            await self._amal_repo.delete_by_ids(
                user_id=user_id, amal_ids=request.deletedAmalIds
            )

        if request.completions:
            await self._completion_repo.upsert_many(
                completions=[self._completion_to_dict(c) for c in request.completions],
                user_id=user_id,
            )

        if request.deletedCompletionIds:
            await self._completion_repo.delete_by_ids(
                user_id=user_id, completion_ids=request.deletedCompletionIds
            )

        amals = await self._amal_repo.get_all_by_user(user_id=user_id)
        completions = await self._completion_repo.get_all_by_user(user_id=user_id)
        categories = await self._category_repo.get_all()
        icons = await self._icon_repo.get_all()

        return AmalSyncResponse(
            amals=[AmalRead.model_validate(amal) for amal in amals],
            completions=[AmalCompletionRead.model_validate(c) for c in completions],
            categories=[AmalCategoryRead.model_validate(cat) for cat in categories],
            icons=[IconRead.model_validate(icon) for icon in icons],
        )

    async def get_all(self, *, user_id: UUID) -> AmalSyncResponse:
        """Get all amals for user without modifying anything."""
        amals = await self._amal_repo.get_all_by_user(user_id=user_id)
        completions = await self._completion_repo.get_all_by_user(user_id=user_id)
        categories = await self._category_repo.get_all()
        icons = await self._icon_repo.get_all()

        return AmalSyncResponse(
            amals=[AmalRead.model_validate(amal) for amal in amals],
            completions=[AmalCompletionRead.model_validate(c) for c in completions],
            categories=[AmalCategoryRead.model_validate(cat) for cat in categories],
            icons=[IconRead.model_validate(icon) for icon in icons],
        )

    @staticmethod
    def _amal_to_dict(amal: AmalCreate, user_id: UUID) -> dict:
        return {
            "id": amal.id,
            "title": amal.title,
            "date": amal.date,
            "time": amal.time,
            "reccuringRule": amal.reccuringRule.name,  # PostgreSQL enum expects uppercase name
            "amalCategoryId": amal.amalCategoryId,
            "iconId": amal.iconId,
            "userId": user_id,
        }

    @staticmethod
    def _completion_to_dict(completion: AmalCompletionCreate) -> dict:
        return {
            "id": completion.id,
            "amalId": completion.amalId,
            "date": completion.date,
            "completedAt": completion.completedAt,
        }
