from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(
        ...,
        description="Human-readable description of the error.",
        example="Resource not found",
    )


class RateLimitExceededResponse(BaseModel):
    detail: str = Field(
        ...,
        description="Message explaining that the request rate limit was exceeded.",
        example="Too many requests. Please retry later.",
    )
    retry_after_seconds: int | None = Field(
        default=None,
        description="Suggested wait time before retrying the request, in seconds.",
        example=60,
    )
