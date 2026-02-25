from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.status import HTTP_200_OK

from app.schemas.response import ResponseModel
from app.services.meta import fetch_meta_data


router = APIRouter(prefix='/metadata')


@router.get(
    '',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
def get_metadata(
    result: Annotated['ResponseModel', Depends(fetch_meta_data)],
) -> ResponseModel:
    return result
