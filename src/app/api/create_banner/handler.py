from typing import Annotated

from fastapi import Header, HTTPException, Request, status

from app.api.create_banner.schemas import (
    CreateBannerRequest,
    CreateBannerResponse
)
from app.system.loging.auth import get_current_user
from app.system.loging.base import ADMIN_NAME


async def create_banner_handler(
    request: Request,
    data_request: CreateBannerRequest,
    token: Annotated[str, Header()],
) -> CreateBannerResponse:
    """Создать баннер."""
    user = await get_current_user(token)

    session = request.app.state.session

    if user.username != ADMIN_NAME:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The user does not have access',
        )

    banner_id = await request.app.state.banner_controller.create_banner(data_request, session)
    return CreateBannerResponse(banner_id=banner_id)
