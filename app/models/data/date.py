
from datetime import (
    date,
    datetime,
)

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    DATE,
    SMALLINT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class DateModel(Base):
    __tablename__ = 'dim_date'
    __table_args__ = {'schema': 'crop_price_dw'}

    id: Mapped[int] = mapped_column(
        type_=BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    full_date: Mapped[date] = mapped_column(
        type_=DATE,
        nullable=False,
        unique=True,
    )

    day: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
        unique=False,
    )

    month: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
        unique=False,
    )

    quarter: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
        unique=False,
    )

    year: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
        unique=False,
    )

    weekday: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
        unique=False,
    )

    is_holiday: Mapped[bool] = mapped_column(
        type_=BOOLEAN,
        nullable=False,
        unique=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
