from app.db.models.user import User
from app.db.cruds.users import get_by_email
from app.services.auth.passwords import hash_password
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

async def create_superuser(
    session: AsyncSession,
    email: str,
    password: str,
    name: Optional[str] = None,
) -> User:
    """Create a superuser with the given credentials."""

    existing_user = await get_by_email(session, email)
    if existing_user:
        if existing_user.is_superuser:
            return existing_user
        else:
            existing_user.is_superuser = True
            await session.commit()
            await session.refresh(existing_user)
            return existing_user

    user = User(
        email=email,
        password=hash_password(password),
        isVerified=True,
        isActive=True,
        isSuperuser=True,
        name=name,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user