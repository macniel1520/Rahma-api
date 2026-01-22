from fastapi import HTTPException, status


def user_not_verified_exc() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": "user_not_verified",
            "message": "Почта не подтверждена.",
        },
    )


# GROUP_NOT_FOUND = HTTPException(
#     status_code=status.HTTP_404_NOT_FOUND,
#     detail={
#         "error": "group_not_found",
#         "message": "Группа не найдена.",
#     },
# )
