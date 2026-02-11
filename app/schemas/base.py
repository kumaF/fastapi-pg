from pydantic import (
    BaseModel,
    ConfigDict,
)


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra='ignore')

    # def build_include_dict(self, paths: list[str] | None) -> dict:
    #     if paths is None:
    #         return {}

    #     if not isinstance(paths, list):
    #         raise TypeError('include must be list[str] | None')

    #     include: dict[str, Any] = {}

    #     for path in paths:
    #         parts = path.split('.')
    #         current = include

    #         for i, part in enumerate(parts):
    #             is_last = i == len(parts) - 1

    #             # Handle array notation: e.g. tags[0], tags[], tags[*]
    #             match = re.match(r'^(\w+)\[(\d+|\*?)\]$', part)
    #             if match:
    #                 field, index = match.groups()
    #                 index = '__all__' if index in ('', '*') else int(index)
    #                 current = current.setdefault(field, {})
    #                 if is_last:
    #                     current[index] = True
    #                 else:
    #                     current = current.setdefault(index, {})
    #             else:
    #                 if is_last:
    #                     current[part] = True
    #                 else:
    #                     current = current.setdefault(part, {})

    #     return include

    # def model_dump(
    #     self,
    #     *,
    #     mode: Literal['json', 'python'] | str = 'python',
    #     include: list[str] | None = None,
    #     exclude: IncEx | None = None,
    #     context: Any | None = None,
    #     by_alias: bool = False,
    #     exclude_unset: bool = False,
    #     exclude_defaults: bool = False,
    #     exclude_none: bool = False,
    #     round_trip: bool = False,
    #     warnings: bool | Literal['none', 'warn', 'error'] = True,
    #     serialize_as_any: bool = False,
    # ):
    #     if include:
    #         include = self.build_include_dict(include)

    #     return super().model_dump(
    #         mode=mode,
    #         by_alias=by_alias,
    #         include=include,
    #         exclude=exclude,
    #         context=context,
    #         exclude_unset=exclude_unset,
    #         exclude_defaults=exclude_defaults,
    #         exclude_none=exclude_none,
    #         round_trip=round_trip,
    #         warnings=warnings,
    #         serialize_as_any=serialize_as_any,
    #     )


__all__ = ['Base']
