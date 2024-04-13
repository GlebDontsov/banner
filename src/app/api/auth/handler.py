from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.system.loging.schemas import Token


async def get_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Получить токен."""
    return await request.app.state.token_controller.login_for_access_token(form_data=form_data)
