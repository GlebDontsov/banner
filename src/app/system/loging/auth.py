from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.system.loging.base import (
    ALGORITHM,
    SECRET_KEY,
    fake_users_db,
    oauth2_scheme,
    pwd_context
)
from app.system.loging.schemas import TokenData, UserInDB


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароли."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)


def get_user(db: dict, username: str) -> Optional[UserInDB]:
    """Возвращает пользователя БД."""
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)
    return None


def authenticate_user(fake_db: dict, username: str, password: str) -> Union[UserInDB, bool]:
    """Проверяет пользователя, если существует возвращает его."""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data_token: dict, expires_delta: timedelta | None = None) -> str:
    """Создает токен."""
    to_encode = data_token.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # noqa: WPS432
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Проверить существует ли пользователь, если да, то вернуть его."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:  # noqa: WPS229
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:  # noqa: WPS329
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
