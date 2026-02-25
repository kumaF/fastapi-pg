from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.types import (
    LanguageCode,
    MetaData,
)
from app.models.data.economic_center import EconomicCenterTranslationModel


class EconomicCenterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_metadata(
        self,
        lang: LanguageCode,
    ) -> list[MetaData]:
        stmt = (
            select(
                EconomicCenterTranslationModel.ref_id,
                EconomicCenterTranslationModel.name
            ).where(EconomicCenterTranslationModel.language_code == lang)
        )
        
        results = await self.session.execute(stmt)
        return results.unique().all()
    