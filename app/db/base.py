from typing import Final

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio.engine import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
    async_sessionmaker,
)

from app.configs import db_configs
from app.core.request import get_request_id


POSTGRES_INDEXES_NAMING_CONVENTION: Final[dict[str, str]] = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}

url_object: URL = URL.create(
    drivername='postgresql+asyncpg',
    username=db_configs.db_user,
    password=db_configs.db_pw,
    host=db_configs.db_host,
    port=db_configs.db_port,
    database=db_configs.db_name,
)

async_engine: AsyncEngine = create_async_engine(
    url=url_object,
    echo=False,
    future=True,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_request_id,
)
