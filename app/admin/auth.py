from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqladmin.authentication import AuthenticationBackend

from app.admin.utils import get_sync_session
from app.db.models.user import User
from app.services.auth.passwords import verify_password


class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.session_factory = get_sync_session()

    async def login(self, request) -> bool:
        """Authenticate user for admin access."""
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        session: Session = self.session_factory()
        try:
            stmt = select(User).where(func.lower(User.email) == func.lower(email))
            result = session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                return False

            if not user.is_superuser or not user.is_active:
                return False

            if not verify_password(password, user.password):
                return False

            request.session.update(
                {
                    "user_id": str(user.id),
                    "user_email": user.email,
                    "is_superuser": user.is_superuser,
                }
            )

            return True

        except Exception:
            return False
        finally:
            session.close()

    async def logout(self, request, response) -> bool:
        """Logout user from admin."""
        request.session.clear()
        return True

    async def authenticate(self, request) -> Optional[dict]:
        """Check if user is authenticated."""
        user_id = request.session.get("user_id")
        is_superuser = request.session.get("is_superuser")

        if not user_id or not is_superuser:
            return None

        return {
            "user_id": user_id,
            "is_superuser": is_superuser,
        }


auth_backend = AdminAuthBackend(secret_key="admin-secret-key-change-in-production")
