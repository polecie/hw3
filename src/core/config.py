import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

config_file = os.getenv("CONFIG_FILE", ".env")


class Config(BaseSettings):
    app_name: str = "REST API for restaurant menu management"
    app_version: str = "0.1.0"
    app_description: str = (
        "This api is designed to implement "
        "all CRUD operations for a restaurant's menu "
        "by providing a range of endpoints "
        "to perform those operations on menu items."
    )
    app_debug: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_expire_in_seconds: int = 60 * 5

    redis_url: str = ""
    redis_report_url: str = ""
    redis_db2: str = ""

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    database_url: str = ""

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str = "guest"
    rabbitmq_default_pass: str = "guest"
    celery_broker_url: str = ""


config = Config(_env_file=config_file, _env_file_encoding="utf-8")  # type: ignore

config.redis_url = f"redis://{config.redis_host}:{config.redis_port}/0"
config.database_url = (
    f"postgresql+asyncpg://{config.postgres_user}"
    f":{config.postgres_password}@{config.postgres_host}"
    f":{config.postgres_port}/{config.postgres_db}"
)
config.celery_broker_url = (
    f"amqp://"
    f"{config.rabbitmq_default_user}:{config.rabbitmq_default_pass}"
    f"@{config.rabbitmq_host}:{config.rabbitmq_port}//"
)
config.redis_db2 = f"redis://{config.redis_host}:{config.redis_port}/2"  # кеш для тестов
config.redis_report_url = f"redis://{config.redis_host}:{config.redis_port}/1"

BASE_DIR = Path(__file__).resolve().parent
