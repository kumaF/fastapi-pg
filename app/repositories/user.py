from sqlalchemy import (
    or_,
    select,
)
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.app.user import (
    UserModel,
    UserProfileModel,
)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data: dict,
    ) -> UserModel:
        db_data = UserModel(**data)

        self.session.add(db_data)

        await self.session.flush()
        await self.session.refresh(db_data)

        return db_data

    async def find_by_id(
        self,
        user_id: str,
    ) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(
                UserModel.id == user_id
            )
        )

        results = await self.session.scalars(stmt)
        return results.unique().one_or_none()
    
    async def find_by_email(
        self,
        email: str,
    ) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(
                UserModel.email == email
            )
        )

        results = await self.session.scalars(stmt)
        return results.unique().one_or_none()
    
    
    async def find_by_identifier(
        self,
        identifier: str,
    ) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(
                or_(
                    UserModel.email == identifier,
                    UserModel.username == identifier,
                ),
                UserModel.is_deleted.is_(False),
            )
        )

        results = await self.session.scalars(stmt)
        return results.unique().one_or_none()
    

    async def update(
        self,
        user_id: str,
        updated_data: dict,
    ) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(
                UserModel.id == user_id,
                UserModel.is_deleted.is_(False),
            )
        )

        results = await self.session.scalars(stmt)
        db_user = results.unique().one_or_none()

        if db_user:
            for field, value in updated_data.items():
                setattr(db_user, field, value)

            await self.session.refresh(db_user)

        return db_user


class UserProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data: dict,
    ) -> UserProfileModel:
        db_data = UserProfileModel(**data)

        self.session.add(db_data)

        await self.session.flush()
        await self.session.refresh(db_data)

        return db_data