from fastapi import HTTPException, status


def user_not_verified_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": "user_not_verified",
            "message": "Email is not verified.",
        },
    )


def invalid_credentials_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "invalid_credentials",
            "message": "Email or password is incorrect.",
        },
    )


def invalid_refresh_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "invalid_refresh",
            "message": "Refresh token invalid/expired.",
        },
    )


def password_mismatch_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "password_mismatch", "message": "Passwords do not match."},
    )


def invalid_code_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "reset_failed", "message": "Invalid code."},
    )


def code_expired_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "reset_failed", "message": "Code expired."},
    )


def verification_failed_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "verification_failed", "message": "Invalid code."},
    )


def verification_expired_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "verification_failed", "message": "Code expired."},
    )


def email_taken_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": "email_taken", "message": "Email already registered."},
    )


def resource_not_found_exc(resource_type: str, resource_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "resource_not_found",
            "message": f"{resource_type} with id {resource_id} not found.",
        },
    )


def jes_timeout_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        detail={"error": "jes_timeout", "message": "JES timeout."},
    )


def jes_network_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail={"error": "jes_network", "message": "JES network error."},
    )


def jes_upstream_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail={"error": "jes_upstream", "message": "JES upstream error."},
    )


def foreign_key_not_found_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "amal_not_found",
            "message": "Amal not found.",
        },
    )
