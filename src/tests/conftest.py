from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
from redis import asyncio as aioredis  # type: ignore
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.controller import TokenController, BannerController
from app.source.base import BannerStorage
from src.app.service import app, prepare_app
from src.app.config.config import Settings
from src.app.models.banner import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: WPS217, WPS210
    """lifespan."""
    global_settings = Settings()
    engine = create_async_engine(global_settings.asyncpg_url_test, future=True, echo=True)
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

app = prepare_app(app)

engine = create_engine(Settings.psycopg2_url_test)

@pytest.fixture(scope='session')
def create_drop_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def client(create_drop_database):
    with TestClient(app) as client:
        yield client
