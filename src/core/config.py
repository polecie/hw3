# import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

env = load_dotenv()


class Config(BaseSettings):
    app_name: str = "test"
    app_version: str = "0.1.0"
    app_description: str = "test"
    app_debug: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_expire_in_seconds: int = 60 * 5

    redis_url: str = f"redis://{redis_host}:{redis_port}/0"
    redis_report_url: str = f"redis://{redis_host}:{redis_port}/1"
    redis_db2: str = f"redis://{redis_host}:{redis_port}/2"  # кеш для тестов

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    database_url: str = (
        f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    )

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str = "guest"
    rabbitmq_default_pass: str = "guest"
    celery_broker_url: str = f"amqp://{rabbitmq_default_user}:{rabbitmq_default_pass}@{rabbitmq_host}:{rabbitmq_port}//"


config = Config(
    # _env_file=env or ".env",
    # _env_file=".env",
    # _env_file_encoding="utf-8"
)

# config.redis_url = f"redis://{config.redis_host}:{config.redis_port}"
# config.database_url = f"postgresql+asyncpg://
# {config.postgres_user}:{config.postgres_password}@
# {config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
# config.celery_broker_url = f"amqp://
# {config.rabbitmq_default_user}:{config.rabbitmq_default_pass}@
# {config.rabbitmq_host}:{config.rabbitmq_port}//"

BASE_DIR = Path(__file__).resolve().parent
