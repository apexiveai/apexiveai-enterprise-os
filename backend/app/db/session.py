from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
)


def check_database() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False


def check_redis() -> bool:
    try:
        return bool(redis_client.ping())
    except RedisError:
        return False


def close_connections() -> None:
    engine.dispose()
    redis_client.close()
