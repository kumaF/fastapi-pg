from datetime import (
    date as _date,
    datetime,
)

from sqlalchemy import (
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    CHAR,
    DATE,
    DOUBLE_PRECISION,
    SMALLINT,
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class PriceDataModel(Base):    
    __tablename__ = 'fact_price_data'
    __table_args__ = (
        Index(
            'idx_fact_price_data_filter_by_crop',
            'date_id',
            'economic_center_id',
            'crop_id',
        ),
        {'schema': 'crop_price_dw'},
    )

    id: Mapped[int] = mapped_column(
        type_=BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    date_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_date.id', ondelete='RESTRICT'),
        type_=BIGINT,
        nullable=False,
    )

    data_source_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_data_source.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_crop_id.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    unit_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_unit.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    economic_center_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_economic_center.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    price_type_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_price_type.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_currency.id', ondelete='RESTRICT'),
        type_=SMALLINT,
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    inserted_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class MVLatestPriceDataModel(Base):    
    __tablename__ = 'mv_latest_crop_prices'
    __table_args__ = {'schema': 'crop_price_dw'}

    id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
    )

    crop: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
    )

    wholesale_price_today: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    wholesale_price_yesterday: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    retail_price_today: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    retail_price_yesterday: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    crop_id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
    )

    economic_center_id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        nullable=False,
    )

    language_code: Mapped[str] = mapped_column(
        type_=CHAR(2),
        primary_key=True,
    )


class MVPastWeekPriceDataModel(Base):    
    __tablename__ = 'mv_past_week_crop_price'
    __table_args__ = {'schema': 'crop_price_dw'}

    date: Mapped[_date] = mapped_column(
        type_=DATE,
        primary_key=True
    )

    wholesale_price: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    retail_price: Mapped[float] = mapped_column(
        type_=DOUBLE_PRECISION,
        nullable=True,
    )

    crop_id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
    )

    economic_center_id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
    )
