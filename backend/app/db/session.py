from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.base import Base


database_url = make_url(settings.database_url)
is_sqlite = database_url.get_backend_name() == "sqlite"

engine_options = {"pool_pre_ping": True}

if is_sqlite:
    engine_options["connect_args"] = {
        "check_same_thread": False,
        "timeout": 30,
    }
else:
    engine_options.update(pool_size=5, max_overflow=10)

engine = create_engine(settings.database_url, **engine_options)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


redis_client = None
redis_available = False

if settings.redis_url:
    try:
        from redis import Redis

        redis_client = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
        redis_available = True
    except ImportError:
        redis_client = None


def check_database() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False


def check_redis() -> bool | None:
    if redis_client is None:
        return None
    try:
        return bool(redis_client.ping())
    except Exception:
        return False


def close_connections() -> None:
    engine.dispose()
    if redis_client is not None:
        redis_client.close()
