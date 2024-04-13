from pydantic import BaseModel, Field

from app.api.user_banner.schemas import UserBannerResponse


class CreateBannerRequest(BaseModel):
    """Схема запроса на создание баннера."""

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


class CreateBannerResponse(BaseModel):
    """Схема успешного ответа создания баннера."""

    banner_id: int = Field(
        ...,
        description='id созданного банера',
        example=0,
    )
