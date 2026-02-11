import asyncio
import logging

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.configs.seed import settings
from app.core.security import hash_password
from app.db.session import get_session
from app.repositories.user import (
    UserProfileRepository,
    UserRepository,
)


if TYPE_CHECKING:
    from app.models.user import UserModel


logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("my_script_logger")

async def seed_initial_user(session: AsyncSession) -> None:
    user_repo = UserRepository(session)
    user_profile_repo = UserProfileRepository(session)

    async with session.begin():
        existing_user = await user_repo.find_by_email(settings.email)

        if not existing_user:    
            db_user: UserModel = await user_repo.create({
                'username': settings.username,
                'email': settings.email,
                'password_hash': hash_password(settings.password),
                'is_active': True,
                'is_verified': True,
            })

            _ = await user_profile_repo.create({
                'user_id': db_user.id,
                'first_name': 'system',
                'last_name': 'admin',
            })

            logger.info('sys-admin user created')
            return

    logger.info('sys user already exists.')


async def main():
    async for session in get_session():
        await seed_initial_user(session)

if __name__ == '__main__':
    asyncio.run(main())