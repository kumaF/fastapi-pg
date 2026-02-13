from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.apikey import ServiceApiKeyModel


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
