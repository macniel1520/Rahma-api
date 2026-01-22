from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.schemas.user.user import UserRead
from app.db.models.user import User
from app.services.auth.current_user import CurrentActiveUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserRead,
    summary="Получение информации о текущем пользователе",
    description="Получение информации о текущем пользователе.",
    response_description="Информация о текущем пользователе",
)
async def get_me(
    user: CurrentActiveUser,
) -> User:
    return user
