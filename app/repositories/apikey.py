from sqlalchemy import (
    func,
    select,
    update,
)
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.app.apikey import ServiceApiKeyModel


class ServiceApiKeyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data: dict,
    ) -> ServiceApiKeyModel:
        db_data = ServiceApiKeyModel(**data)

        self.session.add(db_data)

        await self.session.flush()
        await self.session.refresh(db_data)

        return db_data
    
    async def find_by_key_hash(
        self,
        key_hash: str,
    ) -> ServiceApiKeyModel | None:
        stmt = (
            select(ServiceApiKeyModel)
            .where(
                ServiceApiKeyModel.key_hash == key_hash,
            )
        )

        results = await self.session.scalars(stmt)
        return results.unique().one_or_none()
    
    async def update_last_used_at(
        self,
        key_id: str,
    ) -> None:
        stmt = (
            update(ServiceApiKeyModel)
            .where(ServiceApiKeyModel.id == key_id)
            .values(last_used_at=func.now())
        )

        await self.session.execute(stmt)
        
