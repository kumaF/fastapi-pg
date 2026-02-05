from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import JSONResponse

from app.services.health import health_check_v1


if TYPE_CHECKING:
    from app.schemas.response import ResponseModel

router = APIRouter(prefix='/health')


@router.get('')
def check_health(
    result: Annotated['ResponseModel', Depends(health_check_v1)],
) -> JSONResponse:
    return JSONResponse(
        status_code=result.status,
        content=result.model_dump(exclude_none=True),
    )
