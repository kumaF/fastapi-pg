from fastapi import FastAPI
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api import v1_router
from app.core.lifespan import lifespan
from app.core.middlewares import AddRequestIdMiddleware
from app.errors.handlers import (
    http_db_exception_handler,
    http_exception_handler,
    request_validation_error_handler,
    schema_validation_error_handler,
)
from app.errors.http import HttpDbException


api_prefix: str = '/api'
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(AddRequestIdMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(ValidationError, schema_validation_error_handler)
app.add_exception_handler(HttpDbException, http_db_exception_handler)

app.include_router(v1_router, prefix=api_prefix)
