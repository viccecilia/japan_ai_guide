from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ApiError(BaseModel):
    code: str = Field(description="Stable application error code.")
    message: str = Field(description="Human-readable error message.")


class ApiResponse(BaseModel, Generic[DataT]):
    ok: bool
    data: DataT | None = None
    error: ApiError | None = None
    meta: dict[str, str | int | float | bool] = Field(default_factory=dict)


def success_response(
    data: DataT,
    meta: dict[str, str | int | float | bool] | None = None,
) -> ApiResponse[DataT]:
    return ApiResponse(ok=True, data=data, error=None, meta=meta or {})


def error_response(
    code: str,
    message: str,
    meta: dict[str, str | int | float | bool] | None = None,
) -> ApiResponse[None]:
    return ApiResponse(
        ok=False,
        data=None,
        error=ApiError(code=code, message=message),
        meta=meta or {},
    )
