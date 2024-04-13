from typing import Annotated

from fastapi import Header, HTTPException, Request, status

from app.api.update_banner.schemas import UpdateBannerRequest
from app.system.loging.auth import get_current_user
from app.system.loging.base import ADMIN_NAME


async def update_banner_handler(
    request: Request,
    id: int,  # noqa: WPS125
    data_request: UpdateBannerRequest,
    token: Annotated[str, Header()],
) -> int:
    """Обновить баннер."""
    user = await get_current_user(token)

    session = request.app.state.session

    if user.username != ADMIN_NAME:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The user does not have access',
        )

    await request.app.state.banner_controller.update_banner(id, data_request, session)
    return status.HTTP_200_OK
