from enum import (
    Enum,
    unique,
)
from typing import Literal


class BaseEnum(Enum):
    @classmethod
    def to_dict(
        cls,
        mode: Literal['python', 'json'] = 'python',
    ) -> dict | list:
        return_dict: dict = {}

        if mode == 'python':
            return_dict = {opt.name: opt.value for opt in cls}
        elif mode == 'json':
            return_dict = [{
                'name': opt.name,
                'name_param': getattr(opt, 'unit', opt.name).lower(),
                'name_pretty': opt.name.replace('_', ' ').title(),
                'value': opt.value
            } for opt in cls]
        
        return return_dict

    @classmethod
    def to_list(
        cls,
        mode: Literal['python', 'json'] = 'python'
    ) -> list:
        payload: list = []

        if mode == 'python':
            payload = [opt.value for opt in cls]
        elif mode == 'json':
            payload = [opt.name.lower() for opt in cls]
        
        return payload


@unique
class TokenType(BaseEnum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


@unique
class GrantType(BaseEnum):
    PASSWORD = 'password'
    REFRESH_TOKEN = 'refresh_token'