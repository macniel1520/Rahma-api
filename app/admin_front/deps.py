from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.db.models.user import User
from app.services.auth.current_user import get_current_active_user


async def get_panel_admin_user(user: User = Depends(get_current_active_user)) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только суперпользователь может использовать новую админку.",
        )
    return user


PanelAdminUser = Annotated[User, Depends(get_panel_admin_user)]
