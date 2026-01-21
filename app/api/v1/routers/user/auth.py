from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.schemas.auth.password_reset import (
    RequestResetCodeIn,
    ResetPasswordIn,
)
from app.api.v1.schemas.auth.register import RegisterIn
from app.api.v1.schemas.auth.verification import RequestVerifyIn, VerifyCodeIn
from app.api.v1.schemas.user.user import UserRead
from app.db.engine import get_session
from app.db.models.user import User
from app.services.auth.auth_service import (
    CodeExpired,
    EmailTaken,
    InvalidCode,
    PasswordMismatch,
    register_user,
    request_verify_code as request_verify_code_service,
    verify_code as verify_code_service,
    request_reset_code as request_reset_code_service,
    reset_password as reset_password_service,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterIn,
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        return await register_user(
            session=session,
            email=str(data.email),
            password=data.password,
            name=data.name,
            date_of_birth=data.dateOfBirth,
            gender=data.gender,
            country=data.country,
            avatar_url=data.avatarUrl,
        )
    except EmailTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "email_taken", "message": "Email already registered."},
        )


@router.post("/request-verify-code", status_code=status.HTTP_202_ACCEPTED)
async def request_verify_code(
    data: RequestVerifyIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    await request_verify_code_service(
        session=session,
        email=str(data.email),
    )
    return None


@router.post("/verify-code", response_model=UserRead)
async def verify_code(
    data: VerifyCodeIn,
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        return await verify_code_service(
            session=session,
            email=str(data.email),
            code=data.code,
        )
    except InvalidCode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "verification_failed", "message": "Invalid code."},
        )
    except CodeExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "verification_failed", "message": "Code expired."},
        )


@router.post("/request-reset-code", status_code=status.HTTP_202_ACCEPTED)
async def request_reset_code(
    data: RequestResetCodeIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    await request_reset_code_service(
        session=session,
        email=str(data.email),
    )
    return None


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    data: ResetPasswordIn,
    session: AsyncSession = Depends(get_session),
) -> None:
    try:
        await reset_password_service(
            session=session,
            email=str(data.email),
            code=data.code,
            new_password=data.new_password,
            confirm_password=data.confirm_password,
        )
        return None
    except PasswordMismatch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "password_mismatch", "message": "Passwords do not match."},
        )
    except InvalidCode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "reset_failed", "message": "Invalid code."},
        )
    except CodeExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "reset_failed", "message": "Code expired."},
        )
