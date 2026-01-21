from __future__ import annotations

from app.db.models.user import User
from app.services.auth.tokens import auth_backend

async def issue_access_token(user: User) -> str:
    strategy = auth_backend.get_strategy()
    return await strategy.write_token(user)
