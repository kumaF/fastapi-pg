from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    Field,
    model_validator,
)

from app.schemas.base import BaseSchema


class DataFreshnessResponse(BaseSchema):
    cbsl: datetime
    tz: str = Field(exclude=True)

    @model_validator(mode='after')
    def localize_datetime(self):
        self.cbsl = self.cbsl.astimezone(ZoneInfo(self.tz))

        return self



