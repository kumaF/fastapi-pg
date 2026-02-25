from pydantic import Field

from app.core.types import LanguageCode
from app.schemas.base import BaseSchema


class LatestCropPriceRequestSchema(BaseSchema):
    language_code: LanguageCode = Field(...)
    economic_center_id: int = Field(...)
    crop_ids: list[int] | None = Field(default=None)
    category_ids: list[int] | None = Field(default=None)


class PastWeekCropPriceRequestSchema(BaseSchema):
    economic_center_id: int = Field(...)
    crop_id: int = Field(...)
    