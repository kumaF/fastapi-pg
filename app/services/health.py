from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK

from app.db.session import get_session
from app.db.utils import get_db_response_time_ms
from app.schemas.core import SystemMetrics
from app.schemas.response import ResponseModel
from app.utils import (
    get_api_uptime,
    get_system_metrics,
)


def health_check_v1(
    session: Annotated[AsyncSession, Depends(get_session)],
    uptime: Annotated[str, Depends(get_api_uptime)],
    system_metrics: Annotated[SystemMetrics, Depends(get_system_metrics)],
    db_response_time: Annotated[str, Depends(get_db_response_time_ms)],
) -> ResponseModel:
    return ResponseModel.create_model(
        status=HTTP_200_OK,
        payload={
            'api': 'healthy',
            'version': '1.0.0',
            'uptime': uptime,
            'system_metrics': system_metrics,
            'dependencies': {
                'database': {
                    'status': 'healthy' if session.is_active else 'unhealthy',
                    'response_time_ms': db_response_time,
                }
            },
        },
    )
