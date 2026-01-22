from __future__ import annotations

from fastapi import APIRouter, Depends, status
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
from app.api.v1 import exceptions
from app.docs.responses import (
    invalid_email_taken_response,
    verification_failed_response,
    verification_expired_response,
    password_mismatch_response,
    reset_failed_invalid_code_response,
    reset_failed_code_expired_response,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        **invalid_email_taken_response,  # noqa F405
    },
)
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
        raise exceptions.email_taken_exc()


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


@router.post(
    "/verify-code",
    response_model=UserRead,
    responses={
        **verification_failed_response,  # noqa F405
        **verification_expired_response,  # noqa F405
    },
)
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
        raise exceptions.verification_failed_exc()
    except CodeExpired:
        raise exceptions.verification_expired_exc()


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


@router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **password_mismatch_response,  # noqa F405
        **reset_failed_invalid_code_response,  # noqa F405
        **reset_failed_code_expired_response,  # noqa F405
    },
)
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
        raise exceptions.password_mismatch_exc()
    except InvalidCode:
        raise exceptions.invalid_code_exc()
    except CodeExpired:
        raise exceptions.code_expired_exc()
