from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.status import HTTP_200_OK

from app.schemas.response import ResponseModel
from app.services.health import health_check_v1
    

router = APIRouter(prefix='/health')


@router.get(
    '',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
def check_health(
    result: Annotated['ResponseModel', Depends(health_check_v1)],
) -> ResponseModel:
    return result
