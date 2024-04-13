import os

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv()


class Settings:
    """Secrets."""

    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = int(os.getenv('POSTGRES_PORT'))  # type: ignore
    postgres_db = os.getenv('POSTGRES_DB')
    postgres_db_test = os.getenv('POSTGRES_DB_TEST')

    asyncpg_url = URL.create(
        drivername='postgresql+asyncpg',
        username=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        database=postgres_db,
    )

    psycopg2_url = URL.create(
        drivername='postgresql',
        username=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        database=postgres_db,
    )

    asyncpg_url_test = URL.create(
        drivername='postgresql+asyncpg',
        username=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        database=postgres_db_test,
    )

    psycopg2_url_test = URL.create(
        drivername='postgresql',
        username=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        database=postgres_db_test,
    )

    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
