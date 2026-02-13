from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.schemas.response import ResponseModel
from app.utils.helpers import json_encode_response_model


async def http_exception_handler(
    request: Request,
    e: HTTPException,
) -> JSONResponse:
    _ = request
    content = ResponseModel(status=e.status_code, success=False, message=e.detail)

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content),
        headers=e.headers,
    )


async def schema_validation_error_handler(
    request: Request,
    e: ValidationError,
) -> JSONResponse:
    _ = request
    content = ResponseModel(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        success=False,
        message=f'{e.title.lower()} model validation failed with {str(e.error_count())} errors.',
        errors=json_encode_response_model(e.errors()),
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content),
    )


async def request_validation_error_handler(
    request: Request,
    e: RequestValidationError,
) -> JSONResponse:
    _ = request
    content = ResponseModel(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        success=False,
        message='request body validation failed.',
        errors=json_encode_response_model(e.errors()),
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content),
    )
