from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import JSONResponse

from app.services.auth import generate_access_token


if TYPE_CHECKING:
    from app.schemas.response import ResponseModel

router = APIRouter(prefix='/oauth')


@router.post(path='/token')
async def generate_tokens(
    result: Annotated['ResponseModel', Depends(generate_access_token)],
) -> JSONResponse:
    return JSONResponse(
        status_code=result.status,
        content=result.model_dump(exclude_none=True),
    )
