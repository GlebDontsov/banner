from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.api.user_banner.schemas import UserBannerResponse


class BannerResponse(BaseModel):
    """Схема ответа на запрос баннера по тегу и фиче."""

    banner_id: int = Field(
        ...,
        description='id баннера',
        example=0,
    )

    tag_ids: list[int] = Field(
        ...,
        description='Список тегов',
        example=[0],
    )

    feature_id: int = Field(
        ...,
        description='Фича',
        example=0,
    )

    content: UserBannerResponse = Field(  # noqa: WPS110
        ...,
        description='Контент банера',
    )

    is_active: bool = Field(
        ...,
        description='Действующий банер',
        example=True,
    )

    created_at: datetime = Field(
        ...,
        description='Время создания банера',
        example='2024-04-09 00:51:47.267932',
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description='Время обновления банера',
        example=None,
    )
