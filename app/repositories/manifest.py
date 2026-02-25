from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.data.manifest import MVDataFreshnessModel


class ManifestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_data_freshness(self) -> list[tuple]:
        stmt = select(
            func.max(MVDataFreshnessModel.processed_at)
                .filter(MVDataFreshnessModel.data_source == 'cbsl')
                .label('cbsl')
        )
        
        results = await self.session.execute(stmt)
        return results.mappings().fetchone()
    