from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from app.configs.core import settings
from app.core.exceptions.domain import TokenError
from app.core.security import (
    decode_jwt_header,
    decode_token,
    generate_tokens,
    verify_password,
)
from app.db.session import get_session
from app.db.utils import handle_db_errors
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequestSchema
from app.schemas.enums import (
    GrantType,
    TokenType,
)
from app.schemas.response import ResponseModel
from app.schemas.user import (
    UserCredentialsSchema,
    UserSchema,
)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/oauth/token')


async def generate_access_token(
    session: Annotated[AsyncSession, Depends(get_session)],
    login_request: LoginRequestSchema
) -> ResponseModel:
    if login_request.grant_type == GrantType.PASSWORD:
        return await _password_login(
            credentials=login_request.credentials,
            session=session
        )

    if login_request.grant_type == GrantType.REFRESH_TOKEN:
        return _refresh_token_login(login_request.refresh_token)
    
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Invalid grant type or token',
        headers={'WWW-Authenticate': 'Bearer'}
    )


async def validate_access_token(
    token: Annotated[str, Depends(oauth2_schema)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> tuple[dict, dict]:
    try:
        header: dict = decode_jwt_header(token)

        if header.get('ttyp') != TokenType.ACCESS_TOKEN.value:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid token type. Expected an access token',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        
        payload: dict = decode_token(token)
    except TokenError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
            headers={'WWW-Authenticate': 'Bearer'}
        ) from e
    
    repo = UserRepository(session)

    try:
        db_user = await repo.find_by_id(payload['id'])
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        return ResponseModel.create_model(
            status=err.status_code,
            message=err.message,
            errors=err.errors
        )

    if db_user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication identifier',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    return payload, header


def _refresh_token_login(token: str) -> ResponseModel:
    try:
        header: dict = decode_jwt_header(token)

        if header.get('ttyp') != TokenType.REFRESH_TOKEN.value:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid token type. Expected a refresh token',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        
        payload: dict = decode_token(token)

        to_encode: dict = {
            'id': payload['id'],
            'email': payload['email'],
        }

        access_token, refresh_token = generate_tokens(data=to_encode)

        return ResponseModel.create_model(
            status=HTTP_200_OK,
            payload={
                'token_type': 'bearer',
                'access_token': access_token,
                'expires_in': settings.access_token_exp_delta,
                'refresh_token': refresh_token
            }
        )
    except TokenError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
            headers={'WWW-Authenticate': 'Bearer'}
        ) from e
    
    
async def _password_login(
    credentials: UserCredentialsSchema,
    session: AsyncSession
) -> ResponseModel:
    repo = UserRepository(session)

    try:
        db_user = await repo.find_by_identifier(credentials.identifier)
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        return ResponseModel.create_model(
            status=err.status_code,
            message=err.message,
            errors=err.errors
        )

    if db_user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication identifier',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    verified, updated_pwd = verify_password(
        password=credentials.password,
        hashed_password=db_user.password_hash
    )

    if not verified:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user_data = UserSchema.model_validate(db_user.to_dict())

    if not user_data.is_verified:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='User account is not verified. Please verify your account to proceed.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not user_data.is_active:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='User account is inactive. Please contact support.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if updated_pwd is not None:
        try:
            db_user = await repo.update(
                user_id=db_user.id,
                updated_data={
                    'password_hash': updated_pwd
                }
            )
        except SQLAlchemyError as e:
            err = await handle_db_errors(e)
            return ResponseModel.create_model(
                status=err.status_code,
                message=err.message,
                errors=err.errors
            )

    to_encode: dict = {
        'id': str(db_user.id),
        'email': db_user.email,
    }

    access_token, refresh_token = generate_tokens(data=to_encode)

    return ResponseModel.create_model(
        status=HTTP_200_OK,
        payload={
            'token_type': 'bearer',
            'access_token': access_token,
            'expires_in': settings.access_token_exp_delta,
            'refresh_token': refresh_token
        }
    )