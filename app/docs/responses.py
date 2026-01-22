from app.schemas.error import ErrorResponse
from fastapi import status


def response_error(status_code: int, error: str, message: str):
    return {
        status_code: {
            "model": ErrorResponse,
            "description": message,
            "content": {
                "application/json": {
                    "examples": {
                        "default": {
                            "summary": message,
                            "value": {"error": error, "detail": message},
                        }
                    }
                }
            },
        }
    }


# invalid_group_id_response = response_error(
#     status.HTTP_422_UNPROCESSABLE_ENTITY,
#     "invalid_group_id",
#     "Передан некорректный идентификатор VK группы.",
# )

invalid_email_taken_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "email_taken",
    "Email already registered.",
)

verification_failed_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "verification_failed",
    "Invalid code.",
)

verification_expired_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "verification_failed",
    "Code expired.",
)

user_not_verified_response = response_error(
    status.HTTP_403_FORBIDDEN,
    "user_not_verified",
    "Email is not verified.",
)

invalid_credentials_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "invalid_credentials",
    "Email or password is incorrect.",
)

invalid_refresh_response = response_error(
    status.HTTP_401_UNAUTHORIZED,
    "invalid_refresh",
    "Refresh token invalid/expired.",
)

password_mismatch_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "password_mismatch",
    "Passwords do not match.",
)

reset_failed_invalid_code_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "reset_failed",
    "Invalid code.",
)

reset_failed_code_expired_response = response_error(
    status.HTTP_400_BAD_REQUEST,
    "reset_failed",
    "Code expired.",
)
