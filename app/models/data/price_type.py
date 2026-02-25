
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import (
    CHAR,
    SMALLINT,
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base


class PriceTypeModel(Base):
    __tablename__ = 'dim_price_type'
    __table_args__ = {'schema': 'crop_price_dw'}

    id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=True,
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

    translations: Mapped[list['PriceTypeTranslationModel']] = relationship(
        back_populates='price_type',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )



class PriceTypeTranslationModel(Base):
    __tablename__ = 'price_type_translation'
    __table_args__ = {'schema': 'crop_price_dw'}

    ref_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_price_type.id', ondelete='CASCADE'),
        type_=SMALLINT,
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        type_=CHAR(2),
        primary_key=True,

    )
    name: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=True,
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

    price_type: Mapped['PriceTypeModel'] = relationship(
        back_populates='translations'
    )