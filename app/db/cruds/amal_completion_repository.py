from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.amal import Amal
from app.db.models.amal_completion import AmalCompletion


@runtime_checkable
class AmalCompletionRepository(Protocol):
    async def get_all_by_user(self, *, user_id: UUID) -> Sequence[AmalCompletion]: ...
    async def get_by_ids(
        self, *, completion_ids: list[UUID]
    ) -> Sequence[AmalCompletion]: ...
    async def upsert_many(
        self, *, completions: list[dict], user_id: UUID
    ) -> Sequence[AmalCompletion]: ...
    async def delete_by_ids(
        self, *, user_id: UUID, completion_ids: list[UUID]
    ) -> int: ...


class SqlAlchemyAmalCompletionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_by_user(self, *, user_id: UUID) -> list[AmalCompletion]:
        stmt = (
            select(AmalCompletion)
            .where(AmalCompletion.userId == user_id)
            .order_by(AmalCompletion.date.desc(), AmalCompletion.completedAt.desc())
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_ids(self, *, completion_ids: list[UUID]) -> list[AmalCompletion]:
        if not completion_ids:
            return []
        stmt = select(AmalCompletion).where(AmalCompletion.id.in_(completion_ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def upsert_many(
        self, *, completions: list[dict], user_id: UUID
    ) -> list[AmalCompletion]:
        if not completions:
            return []

        # Validate that all amalIds belong to the user
        amal_ids = list({c["amalId"] for c in completions})
        valid_amal_ids_result = await self._session.scalars(
            select(Amal.id).where(Amal.id.in_(amal_ids), Amal.userId == user_id)
        )
        valid_amal_ids = set(valid_amal_ids_result.all())

        # Filter out completions for amals that don't belong to user
        valid_completions = [c for c in completions if c["amalId"] in valid_amal_ids]

        if not valid_completions:
            return []

        # Add userId to each completion
        for c in valid_completions:
            c["userId"] = user_id

        stmt = insert(AmalCompletion).values(valid_completions)
        stmt = stmt.on_conflict_do_update(
            index_elements=[AmalCompletion.id],
            set_={
                "amalId": stmt.excluded.amalId,
                "date": stmt.excluded.date,
                "completedAt": stmt.excluded.completedAt,
            },
        )
        await self._session.execute(stmt)
        await self._session.flush()

        completion_ids = [c["id"] for c in valid_completions]
        return await self.get_by_ids(completion_ids=completion_ids)

    async def delete_by_ids(self, *, user_id: UUID, completion_ids: list[UUID]) -> int:
        """Delete specific completions by IDs (only if they belong to user)."""
        if not completion_ids:
            return 0
        stmt = delete(AmalCompletion).where(
            AmalCompletion.userId == user_id,
            AmalCompletion.id.in_(completion_ids),
        )
        result = await self._session.execute(stmt)
        return result.rowcount
