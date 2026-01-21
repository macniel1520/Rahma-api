from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.db.models.user import User
from app.api.v1.schemas.user.user import UserRead, UserUpdate
from app.services.auth.tokens import auth_backend
from app.services.auth.user_manager import get_user_manager

router = APIRouter(prefix="/users", tags=["users"])

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
