import base64
import datetime as dt
import hashlib
import hmac
import json
import secrets

from datetime import (
    date,
    datetime,
    timedelta,
)
from time import time
from uuid import uuid4

import jwt

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    PyJWTError,
)
from passlib.context import CryptContext

from app.configs.core import settings
from app.errors.domain import (
    CursorError,
    TokenError,
)
from app.schemas.enums import TokenType


pwd_context = CryptContext(
    # append the hash(es) list you wish to support.
    schemes=['argon2'],
    # if not mentioned it will use the first hasher in the schemes list.
    default='argon2',
    # either you can specify hasher list you need to depricate
    # or 'auto' mark all but first hasher in schemes list as deprecated
    deprecated='auto'
)

def _sign(data: bytes) -> str:
    return hmac.new(
        settings.secret_key.encode(),
        data,
        hashlib.sha256,
    ).hexdigest()


def encode_cursor(
    expires_in_seconds: int,
    cursor_id: int | None = None,
    cursor_date: date | None = None,
) -> str:
    payload = {
        'exp': int(time()) + expires_in_seconds,
    }

    if cursor_id:
        payload.update({
            'id': cursor_id,
        })

    if cursor_date:
        payload.update({
            'cursor_date': cursor_date.isoformat(),
        })

    raw = json.dumps(payload, separators=(",", ":")).encode()
    encoded = base64.urlsafe_b64encode(raw).decode()
    signature = _sign(raw)

    return f"{encoded}.{signature}"


def decode_cursor(cursor: str) -> tuple[date | None, int | None]:
    try:
        encoded, signature = cursor.split('.')

        raw = base64.urlsafe_b64decode(encoded.encode())

        expected_sig = _sign(raw)
        if not hmac.compare_digest(signature, expected_sig):
            msg: str = 'Cursor signature invalid'
            raise CursorError(msg)

        payload: dict = json.loads(raw)

        if 'exp' in payload and time() > payload['exp']:
            msg: str = 'Cursor expired'
            raise CursorError(msg)

        cursor_id = payload.get('id')

        if payload.get('cursor_date'):
            cursor_date = datetime.fromisoformat(payload['cursor_date'])
        else:
            cursor_date = None

        return ( cursor_date, cursor_id, )
    except Exception as e:
        raise CursorError('Invalid cursor') from e


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)


def verify_password(
    password: str,
    hashed_password: str
) -> tuple[bool, str | None]:
    is_verified, updated_password = pwd_context.verify_and_update(
        secret=password,
        hash=hashed_password
    )

    return is_verified, updated_password


def _generate_jwt_token(
    data: dict,
    token_type: TokenType,
    exp_delta: int | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(dt.UTC) + timedelta(minutes=exp_delta)

    to_encode.update({
        'exp': expire,
        'nbf': datetime.now(dt.UTC),
        'iss': settings.token_issuer,
        'iat': datetime.now(dt.UTC),
        'sub': to_encode['id'],
        'aud': settings.token_audience,
        'jti': uuid4().hex
    })

    return jwt.encode(
        payload=to_encode,
        algorithm=settings.token_algorithm,
        key=base64.b64decode(settings.private_key),
        headers={'ttyp': token_type.value}
    )


def generate_tokens(data: dict) -> tuple[str, str]:
    access_token: str = _generate_jwt_token(
        data=data,
        token_type=TokenType.ACCESS_TOKEN,
        exp_delta=settings.access_token_exp_delta
    )

    refresh_token: str = _generate_jwt_token(
        data=data,
        token_type=TokenType.REFRESH_TOKEN,
        exp_delta=settings.refresh_token_exp_delta
    )

    return access_token, refresh_token


def decode_jwt_header(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)

        if not isinstance(header, dict):
            msg: str = 'jwt header is not a json object'
            raise TokenError(msg)
        
        return header  # noqa: TRY300
    except PyJWTError as e:
        msg: str = 'invalid jwt header'
        raise TokenError(msg) from e
    

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            algorithms=[settings.token_algorithm],
            key=base64.b64decode(settings.public_key),
            audience=settings.token_audience,
            issuer=settings.token_issuer,
            options={
                'verify_signature': True,
                'require': ['exp', 'iat', 'nbf', 'iss', 'jti', 'aud']
            }
        )
    except ExpiredSignatureError as e:
        msg: str = 'Token has expired'
        raise TokenError(msg) from e
    except InvalidTokenError as e:
        msg: str = 'Invalid token'
        raise TokenError(msg) from e
    