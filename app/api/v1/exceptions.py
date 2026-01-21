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
            detail={"error": "invalid_credentials",
             "message": "Email or password is incorrect."},
        )

def invalid_refresh_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_refresh",
                "message": "Refresh token invalid/expired.",
            },
        )