from fastapi import FastAPI, status

from app.api.auth.handler import get_access_token
from app.api.banner.handler import get_banners_handler
from app.api.banner.schemas import BannerResponse
from app.api.create_banner.handler import create_banner_handler
from app.api.create_banner.schemas import CreateBannerResponse
from app.api.delete_banner.handler import delete_banner_handler
from app.api.healthz.ready import ready
from app.api.update_banner.handler import update_banner_handler
from app.api.user_banner.handler import user_banner_handler
from app.api.user_banner.schemas import UserBannerResponse
from app.system.loging.schemas import Token


def setup_routes(app: FastAPI) -> None:
    """Инициализирует маршруты приложения."""
    app.router.api_route(
        path='/healthz/ready',
        methods=['GET'],
    )(ready)

    app.router.api_route(
        path='/token',
        methods=['POST'],
        response_model=Token,
    )(get_access_token)

    app.router.api_route(
        path='/user_banner',
        methods=['GET'],
        response_model=UserBannerResponse,
    )(user_banner_handler)

    app.router.api_route(
        path='/banner',
        methods=['GET'],
        response_model=list[BannerResponse],
    )(get_banners_handler)

    app.router.api_route(
        path='/banner',
        methods=['POST'],
        response_model=CreateBannerResponse,
        status_code=status.HTTP_201_CREATED
    )(create_banner_handler)

    app.router.api_route(
        path='/banner/{id}',
        methods=['PATCH'],
    )(update_banner_handler)

    app.router.api_route(
        path='/banner/{id}',
        methods=['DELETE'],
    )(delete_banner_handler)
