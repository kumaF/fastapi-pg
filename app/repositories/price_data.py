from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.types import LanguageCode
from app.models.data.price_data import (
    MVLatestPriceDataModel,
    MVPastWeekPriceDataModel,
)


class PriceDataRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_latest_price_data(
        self,
        lang_code: LanguageCode,
        economic_center_id: int,
        crop_ids: list[int] | None,
        category_ids: list[int] | None,
        cursor_id: int | None,
        limit: int = 10,
    ) -> list[MVLatestPriceDataModel]:
        stmt = (
            select(MVLatestPriceDataModel)
            .where(
                MVLatestPriceDataModel.language_code == lang_code,
                MVLatestPriceDataModel.economic_center_id == economic_center_id,
            )
            .order_by(
                MVLatestPriceDataModel.id
            )
            .limit(limit)
        )

        if crop_ids:
            stmt = stmt.where(
                MVLatestPriceDataModel.crop_id.in_(crop_ids)
            )
        
        if category_ids:
            stmt = stmt.where(
                MVLatestPriceDataModel.category_id.in_(category_ids)
            )
        
        if cursor_id:
            stmt = (
                stmt
                .where(
                    MVLatestPriceDataModel.id > cursor_id
                )
            )

        results = await self.session.scalars(stmt)
        return results.unique().all()
    

    async def find_past_week_price_data(
        self,
        economic_center_id: int,
        crop_id: list[int] | None,
        cursor_date: date | None,
        limit: int = 10,
    ) -> list[MVPastWeekPriceDataModel]:
        stmt = (
            select(MVPastWeekPriceDataModel)
            .where(
                MVPastWeekPriceDataModel.crop_id == crop_id,
                MVPastWeekPriceDataModel.economic_center_id == economic_center_id,
            )
            .order_by(
                MVPastWeekPriceDataModel.date.desc()
            )
            .limit(limit)
        )

        if cursor_date:
            stmt = (
                stmt
                .where(
                    MVPastWeekPriceDataModel.date < cursor_date
                )
            )

        results = await self.session.scalars(stmt)
        return results.unique().all()
    