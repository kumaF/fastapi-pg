import inspect as property_inspect

from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.inspection import inspect as column_inspect
from sqlalchemy.orm import DeclarativeBase

from app.db.base import POSTGRES_INDEXES_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION, schema='public'
    )

    __table_args__ = {'schema': 'public'}

    def get_model_columns(self):
        return [column.key for column in column_inspect(self).mapper.column_attrs]

    def get_model_properties(self):
        return [
            name
            for name in dir(self)
            if isinstance(property_inspect.getattr_static(self, name), property)
        ]

    def get_model_hybrid_properties(self):
        return [
            name
            for name in dir(self)
            if isinstance(property_inspect.getattr_static(self, name), hybrid_property)
        ]

    def get_columns_and_properties(self):
        columns = self.get_model_columns()
        properties = self.get_model_properties()
        hybrid_properties = self.get_model_hybrid_properties()

        return [*columns, *properties, *hybrid_properties]

    def to_dict(self, include: list | None = None, exclude: list | None = None):
        if bool(include) and not isinstance(include, list):
            raise TypeError("The 'include' argument must be a valid list or None")

        if bool(exclude) and not isinstance(exclude, list):
            raise TypeError("The 'exclude' argument must be a valid list or None")

        result = {}

        for column in self.get_columns_and_properties():
            if include and column not in include:
                continue
            if exclude and column in exclude:
                continue

            value = getattr(self, column)

            if isinstance(value, Base):
                result[column] = value.to_dict()
            elif isinstance(value, list) and value and isinstance(value[0], Base):
                result[column] = [item.to_dict() for item in value]
            else:
                result[column] = value

        return result
