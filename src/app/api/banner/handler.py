from typing import Annotated, Optional

from fastapi import Header, HTTPException, Request, status

from app.api.banner.schemas import BannerResponse
from app.system.loging.auth import get_current_user
from app.system.loging.base import ADMIN_NAME


async def get_banners_handler(  # noqa: WPS211
    request: Request,
    token: Annotated[str, Header()],
    tag_id: Optional[int] = None,
    feature_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> list[BannerResponse]:
    """Получить баннер по фиче и тегу."""
    user = await get_current_user(token)

    session = request.app.state.session

    if user.username != ADMIN_NAME:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The user does not have access',
        )
    return await request.app.state.banner_controller.get_banners(
        tag_id, feature_id, limit, offset, session,
    )
