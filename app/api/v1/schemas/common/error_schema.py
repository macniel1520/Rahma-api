from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")


class ErrorResponse(BaseModel):
    detail: ErrorDetail = Field(..., description="Error details")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": {
                        "error": "resource_not_found",
                        "message": "Route with id 123e4567-e89b-12d3-a456-426614174000 not found.",
                    }
                }
            ]
        }
    }
