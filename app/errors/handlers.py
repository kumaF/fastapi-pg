from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.errors.http import HttpDbException
from app.schemas.response import ResponseModel
from app.utils.helpers import json_encode_response_model


async def http_exception_handler(
    request: Request,
    e: HTTPException,
) -> JSONResponse:
    _ = request

    content = ResponseModel.create_model(
        status=e.status_code,
        message=e.detail
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content, exclude_none=True),
        headers=e.headers,
    )

async def http_db_exception_handler(
    request: Request,
    e: HttpDbException,
) -> JSONResponse:
    _ = request

    content = ResponseModel.create_model(
        status=e.status_code,
        message=e.message,
        errors=e.errors,
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content, exclude_none=True),
        headers=e.headers,
    )

async def schema_validation_error_handler(
    request: Request,
    e: ValidationError,
) -> JSONResponse:
    _ = request
    content = ResponseModel.create_model(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        message=f'{e.title.lower()} model validation failed with {str(e.error_count())} errors.',
        errors=json_encode_response_model(e.errors()),
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content, exclude_none=True),
    )


async def request_validation_error_handler(
    request: Request,
    e: RequestValidationError,
) -> JSONResponse:
    _ = request

    content = ResponseModel.create_model(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        message='request validation failed.',
        errors=json_encode_response_model(e.errors()),
    )

    return JSONResponse(
        status_code=content.status,
        content=json_encode_response_model(content, exclude_none=True),
    )
