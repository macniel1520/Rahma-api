from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.auth.session import RefreshIn, LogoutIn, TokenPairOut, LoginIn
from app.api.v1.exceptions import invalid_credentials_exc, invalid_refresh_exc
from app.db.engine import get_session
from app.services.auth.auth_service import login_with_email_password, InvalidCredentials
from app.services.auth.tokens import rotate_refresh, revoke_refresh, InvalidRefresh

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPairOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
):
    try:
        tokens = await login_with_email_password(
            session=session,
            email=str(data.email),
            password=data.password,
        )
        return tokens
    except InvalidCredentials:
        raise invalid_credentials_exc()

@router.post("/refresh", response_model=TokenPairOut)
async def refresh(
    data: RefreshIn,
    session: AsyncSession = Depends(get_session),
):
    try:
        pair = await rotate_refresh(session, refresh_token=data.refresh_token)
        return TokenPairOut(
            access_token=pair.access_token,
            refresh_token=pair.refresh_token,
        )
    except InvalidRefresh:
        raise invalid_refresh_exc()

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    data: LogoutIn,
    session: AsyncSession = Depends(get_session),
):
    await revoke_refresh(session, refresh_token=data.refresh_token)
    return None
