from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.banner.schemas import BannerResponse
from app.api.create_banner.schemas import CreateBannerRequest
from app.api.update_banner.schemas import UpdateBannerRequest
from app.api.user_banner.schemas import UserBannerModel, UserBannerResponse
from app.models.banner import Banner, BannerTagsFeature


class BannerStorage:
    """Запросы в БД постгрес."""

    async def is_banner(
        self,
        feature_id: int,
        tag_ids: list,
        session: AsyncSession,
        banner_id: int = 0,
    ) -> Optional[bool]:
        """Получает баннер из списка."""
        for tag_id in tag_ids:
            tag_feature_banner_exist = await session.execute(
                select(BannerTagsFeature).where(
                    (BannerTagsFeature.feature_id == feature_id) & (BannerTagsFeature.tag_ids == tag_id)  # noqa: E501, WPS465
                )
            )
            tag_feature_banner_exist = tag_feature_banner_exist.scalars().first()
            if tag_feature_banner_exist and tag_feature_banner_exist.banner_id != banner_id:
                return True
        return None

    async def create(self, data_request: CreateBannerRequest, session: AsyncSession) -> int:
        """Создает баннер."""
        result_exist = await self.is_banner(data_request.feature_id, data_request.tag_ids, session)
        if result_exist:
            raise HTTPException(status_code=422, detail='Banner already exist')

        banner = Banner(
            feature_id=data_request.feature_id,
            tag_ids=data_request.tag_ids,
            title=data_request.content.title,
            text=data_request.content.text,
            url=str(data_request.content.url),
            is_active=data_request.is_active,
        )

        session.add(banner)

        await session.flush()

        banner_id = banner.id

        for tag_id in data_request.tag_ids:
            tag_feature_banner = BannerTagsFeature(
                banner_id=banner_id,
                feature_id=data_request.feature_id,
                tag_ids=tag_id,
            )
            session.add(tag_feature_banner)

        await session.commit()

        return banner_id

    async def delete(self, id: int, session: AsyncSession) -> None:
        """Удаляет баннер."""
        current_banner = await session.execute(select(Banner).where(Banner.id == id))  # noqa:WPS221
        current_banner = current_banner.scalars().first()  # type: ignore
        if not current_banner:
            raise HTTPException(status_code=404, detail='The banner was not found')
        await session.delete(current_banner)
        await session.commit()

    async def update(
        self,
        id: int,
        data_request: UpdateBannerRequest,
        session: AsyncSession,
    ) -> None:
        """Обновляет банер."""
        current_banner = await session.execute(select(Banner).where(Banner.id == id))  # noqa:WPS221
        current_banner = current_banner.scalars().first()  # type: ignore
        if not current_banner:
            raise HTTPException(status_code=404, detail='The banner was not found')

        current_banner.tag_ids = data_request.tag_ids
        current_banner.title = data_request.content.title
        current_banner.text = data_request.content.text
        current_banner.url = str(data_request.content.url)
        current_banner.feature_id = data_request.feature_id
        current_banner.is_active = data_request.is_active
        current_banner.updated_at = datetime.now()

        result_exist = await self.is_banner(
            data_request.feature_id,
            data_request.tag_ids,
            session,
            id,
        )

        if result_exist:
            raise HTTPException(status_code=422, detail='Banner already exist')

        await session.execute(delete(BannerTagsFeature).where(BannerTagsFeature.banner_id == id))
        await session.commit()

        for tag_id in data_request.tag_ids:
            tag_feature_banner = BannerTagsFeature(
                banner_id=id,
                feature_id=data_request.feature_id,
                tag_ids=tag_id,
            )
            session.add(tag_feature_banner)

        await session.commit()

    async def get_banners(  # noqa: WPS211
        self,
        tag_id: Optional[int],
        feature_id: Optional[int],
        limit: int,
        offset: int,
        session: AsyncSession,
    ) -> list[BannerResponse]:
        """Получает список баннеров по теги и/или фиче."""
        if feature_id is None:
            query = select(Banner).where(
                Banner.tag_ids.contains([tag_id]),
            ).limit(limit).offset(offset)
            result_banners = await session.execute(query)
            banners = result_banners.scalars().all()
        elif tag_id is None:
            query = select(Banner).where(
                Banner.feature_id == feature_id,
            ).limit(limit).offset(offset)
            result_banners = await session.execute(query)
            banners = result_banners.scalars().all()
        else:
            query = select(Banner).where(or_(
                Banner.feature_id == feature_id,
                Banner.tag_ids.contains([tag_id]),
            )
            ).limit(limit).offset(offset)
            result_banners = await session.execute(query)
            banners = result_banners.scalars().all()
        lst_banners = []
        for banner in banners:
            lst_banners.append(BannerResponse(
                banner_id=banner.id,
                tag_ids=banner.tag_ids,
                feature_id=banner.feature_id,
                content=UserBannerResponse(title=banner.title, text=banner.text, url=banner.url),
                is_active=banner.is_active,
                created_at=banner.created_at,
                updated_at=banner.updated_at,
            )
            )

        return lst_banners

    async def get_banner_content(
        self,
        tag_id: int,
        feature_id: int,
        session: AsyncSession,
    ) -> UserBannerModel:
        """Получить контент банера по фиче и тегу."""
        banner = await session.execute(
            select(BannerTagsFeature).where(
                (BannerTagsFeature.feature_id == feature_id) & (BannerTagsFeature.tag_ids == tag_id)  # noqa: E501, WPS465
            )
        )
        banner = banner.scalars().first()

        if not banner:
            raise HTTPException(status_code=404, detail='The banner was not found')

        banner_id = banner.banner_id
        banner = await session.execute(select(Banner).where(Banner.id == banner_id))  # noqa:WPS221
        banner = banner.scalars().first()

        return UserBannerModel(
            title=banner.title,
            text=banner.text,
            url=banner.url,
            is_active=banner.is_active,
        )
