from app.schemas.error import ErrorResponse


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
