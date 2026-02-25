from typing import Literal


AttributeType = Literal[
    'data_source',
    'crop',
    'crop_category',
    'economic_center',
    'price_type',
]

LanguageCode = Literal[
    'en',
    'ta',
    'si',
]

MetaData = tuple[int, str]

PriceChangeDirection = Literal[
    'up',
    'down',
    'no_change',
]