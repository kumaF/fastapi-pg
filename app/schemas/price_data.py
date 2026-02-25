import datetime as dt

from datetime import (
    date as _date,
    datetime,
)
from typing import Self

from pydantic import Field

from app.core.types import PriceChangeDirection
from app.models.data.price_data import MVLatestPriceDataModel
from app.schemas.base import BaseSchema


class PriceChange(BaseSchema):
    direction: PriceChangeDirection | None
    value: float | None
    percentage: float | None

    @classmethod
    def create_model(
        cls,
        *,
        today: float | None,
        yesterday: float | None,
    ) -> Self:
        direction: PriceChangeDirection | None = None
        value: float | None = None
        percentage: float | None = None

        if (today and yesterday):
            value = today - yesterday
            percentage = (value / yesterday) * 100
            direction = 'no_change' if value == 0 else 'up' if value > 0 else 'down'
        
        return cls(
            direction=direction,
            value=value,
            percentage=float(f"{percentage:.2f}") if percentage is not None else percentage,
        )


class MarketPrice(BaseSchema):
    today: float | None
    yesterday: float | None
    change: PriceChange

    @classmethod
    def create_model(
        cls,
        *,
        today: float | None,
        yesterday: float | None,
    ) -> Self:
        change = PriceChange.create_model(
            today=today,
            yesterday=yesterday,
        )
        
        return cls(
            today=today,
            yesterday=yesterday,
            change=change
        )


class ContextInfo(BaseSchema):
    id: int
    value: str


class PriceCardContext(BaseSchema):
    crop: ContextInfo
    unit: str

    @classmethod
    def create_model(
        cls,
        *,
        crop_id: int,
        crop_val: str,
        unit: str,
    ) -> Self:
        return cls(
            crop=ContextInfo(
                id=crop_id,
                value=crop_val,
            ),
            unit=unit,
        )

class PriceSet(BaseSchema):
    wholesale: MarketPrice
    retail: MarketPrice

    @classmethod
    def create_model(
        cls,
        *,
        wholesale_price_today: float | None,
        wholesale_price_yesterday: float | None,
        retail_price_today: float | None,
        retail_price_yesterday: float | None
    ) -> Self:
        wholesale = MarketPrice.create_model(
            today=wholesale_price_today,
            yesterday=wholesale_price_yesterday,
        )

        retail = MarketPrice.create_model(
            today=retail_price_today,
            yesterday=retail_price_yesterday,
        )

        return cls(
            wholesale=wholesale,
            retail=retail,
        )


class PriceCard(BaseSchema):
    context: PriceCardContext
    price: PriceSet

    @classmethod
    def create_model(
        cls,
        *,
        item: MVLatestPriceDataModel,
    ) -> Self:
        context = PriceCardContext.create_model(
            crop_id=item.crop_id,
            crop_val=item.crop,
            unit=item.unit,
        )

        price = PriceSet.create_model(
            wholesale_price_today=item.wholesale_price_today,
            wholesale_price_yesterday=item.wholesale_price_yesterday,
            retail_price_today=item.retail_price_today,
            retail_price_yesterday=item.retail_price_yesterday,
        )
        
        return cls(
            context=context,
            price=price,
        )


class PastWeekPriceDataResponse(BaseSchema):
    date: _date
    wholesale_price: float | None
    retail_price: float | None
