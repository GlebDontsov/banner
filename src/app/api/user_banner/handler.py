from typing import Annotated, Optional

from fastapi import Header, HTTPException, Request, status

from app.api.user_banner.schemas import UserBannerResponse
from app.system.loging.auth import get_current_user
from app.system.loging.base import ADMIN_NAME


async def user_banner_handler(  # noqa: WPS231
    request: Request,
    tag_id: int,
    feature_id: int,
    token: Annotated[str, Header()],
    use_last_revision: Optional[bool] = None,
) -> UserBannerResponse:
    """Возвращает баннер."""
    user = await get_current_user(token)

    session = request.app.state.session
    redis = request.app.state.redis

    if user.username != ADMIN_NAME and use_last_revision:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The user does not have access',
        )
    elif user.username == ADMIN_NAME and use_last_revision:
        return await request.app.state.banner_controller.get_banner_content(
            tag_id, feature_id, session,
        )
    elif not use_last_revision:
        return await request.app.state.banner_controller.get_banner_content_cache(
            tag_id, feature_id, user.username, session, redis,
        )
