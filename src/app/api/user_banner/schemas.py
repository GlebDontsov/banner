from pydantic import AnyUrl, BaseModel, Field


class UserBannerResponse(BaseModel):
    """Контент баннера."""

    title: str = Field(
        ...,
        description='Титул',
        example='some_title',
    )

    text: str = Field(
        ...,
        description='Текст',
        example='some_text'
    )

    url: AnyUrl = Field(
        ...,
        description='url',
        example='https://www.google.com/',
    )


class UserBannerModel(UserBannerResponse):
    """Мдодель ответа контента баннера с полем is_active."""

    is_active: bool = Field(
        ...,
        description='Действующий банер',
        example=True,
    )
