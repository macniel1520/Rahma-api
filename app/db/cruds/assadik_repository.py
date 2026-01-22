from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.enums import Role
from app.db.models.message import Message


@runtime_checkable
class AssadikRepository(Protocol):
    async def add_message(
        self, *, content: str, role: Role, user_id: UUID
    ) -> Message: ...


class SqlAlchemyAssadikRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, *, content: str, role: Role, user_id: UUID) -> Message:
        message = Message(content=content, role=role, userId=user_id)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message
