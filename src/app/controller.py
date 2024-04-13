import logging
import pickle  # noqa: S403
from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.banner.schemas import BannerResponse
from app.api.create_banner.schemas import CreateBannerRequest
from app.api.update_banner.schemas import UpdateBannerRequest
from app.api.user_banner.schemas import UserBannerResponse
from app.source.base import BannerStorage
from app.system.loging.auth import (
    authenticate_user,
    create_access_token,
    fake_users_db
)
from app.system.loging.base import ACCESS_TOKEN_EXPIRE_MINUTES, ADMIN_NAME
from app.system.loging.schemas import Token

logging.basicConfig(level=logging.INFO)


class TokenController:
    """Контроллер для операций с токеном."""

    async def login_for_access_token(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> Token:
        """Возвращает токен пользователю."""
        user = authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data_token={'sub': user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type='bearer')  # noqa: S106


class BannerController:
    """Контроллер для операций с баннером."""

    def __init__(self, storage: BannerStorage):
        self.storage = storage

    async def create_banner(self, data_request: CreateBannerRequest, session: AsyncSession) -> int:
        """Создание баннера."""
        return await self.storage.create(data_request, session)

    async def delete_banner(self, id: int, session: AsyncSession) -> None:
        """Удаление баннера."""
        await self.storage.delete(id, session)

    async def update_banner(
        self,
        id: int,
        data_request: UpdateBannerRequest,
        session: AsyncSession,
    ) -> None:
        """Обновление баннера."""
        await self.storage.update(id, data_request, session)

    async def get_banners(  # noqa: WPS211
        self,
        tag_id: Optional[int],
        feature_id: Optional[int],
        limit: int,
        offset: int,
        session: AsyncSession,
    ) -> list[BannerResponse]:
        """Получает список баннеров по фиче и/или тегу."""
        if tag_id is None and feature_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='tag_id and feature_id not exist',
            )

        return await self.storage.get_banners(tag_id, feature_id, limit, offset, session)

    async def get_banner_content(
        self,
        tag_id: int,
        feature_id: int,
        session: AsyncSession,
    ) -> UserBannerResponse:
        """Пулучить содержимое баннера."""
        return await self.storage.get_banner_content(tag_id, feature_id, session)

    async def get_banner_content_cache(  # noqa: WPS211
        self,
        tag_id: int,
        feature_id: int,
        username: str,
        session: AsyncSession,
        redis: Redis,
    ) -> UserBannerResponse:
        """Пулучить содержимое баннера с хеша."""
        key_word = f'{tag_id}s{feature_id}'
        cache = await redis.get(key_word)
        if cache is not None:
            logging.info('Данные из кеша')
            response_data = pickle.loads(cache.encode('latin1'))  # noqa: S301
            if response_data.is_active is False and username != ADMIN_NAME:
                raise HTTPException(status_code=404, detail='The banner is unavailable')
            return UserBannerResponse(
                title=response_data.title,
                text=response_data.text,
                url=response_data.url,
            )

        response_data = await self.storage.get_banner_content(tag_id, feature_id, session)

        await redis.set(key_word, pickle.dumps(response_data).decode('latin1'))
        await redis.expire(key_word, 60 * 5)

        if response_data.is_active is False and username != ADMIN_NAME:
            raise HTTPException(status_code=404, detail='The banner is unavailable')

        return UserBannerResponse(
            title=response_data.title,
            text=response_data.text,
            url=response_data.url,
        )
