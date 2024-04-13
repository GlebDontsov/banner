import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis  # type: ignore
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.api.routes import setup_routes
from app.config.config import Settings
from app.controller import BannerController, TokenController
from app.source.base import BannerStorage

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: WPS217, WPS210
    """lifespan."""
    global_settings = Settings()
    engine = create_async_engine(global_settings.asyncpg_url, future=True, echo=True)
    session_local = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    session = session_local()

    redis = aioredis.from_url(
        f'redis://{global_settings.redis_host}:{global_settings.redis_port}',
        encoding='utf8',
        decode_responses=True,
    )

    storage = BannerStorage()

    app.state.session = session
    app.state.redis = redis
    app.state.token_controller = TokenController()
    app.state.banner_controller = BannerController(storage)

    yield

    await session.close()
    await redis.close()


app = FastAPI(lifespan=lifespan)


def prepare_app(app_fastapi: FastAPI) -> FastAPI:
    """Настроить экхемпляр приложения FastAPI."""
    setup_routes(app_fastapi)
    app_fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],  # Разрешить доступ из любого источника
        allow_credentials=True,  # Разрешить отправку куки и заголовков аутентификации
        allow_methods=['*'],  # Разрешить все HTTP-методы
        allow_headers=['*'],  # Разрешить все заголовки
    )

    return app_fastapi


if __name__ == '__main__':
    uvicorn.run(
        app=prepare_app(app),
        host=os.getenv('HOST'),  # type: ignore
        port=int(os.getenv('PORT')),  # type: ignore
    )
