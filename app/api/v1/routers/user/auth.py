from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.db.models.user import User
from app.api.v1.schemas.user.user import UserRead, UserCreate, UserUpdate
from app.services.auth.tokens import auth_backend
from app.services.auth.user_manager import get_user_manager

router = APIRouter(prefix="/auth", tags=["auth"])

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)
