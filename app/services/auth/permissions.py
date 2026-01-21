from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi_users import FastAPIUsers

from app.db.models.user import User
from app.services.auth.tokens import auth_backend
from app.services.auth.user_manager import get_user_manager


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

CurrentActiveUser = Annotated[User, Depends(current_active_user)]
CurrentVerifiedUser = Annotated[User, Depends(current_verified_user)]
CurrentSuperUser = Annotated[User, Depends(current_superuser)]
