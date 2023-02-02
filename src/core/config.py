from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

app_name: str = "test"  # type: ignore
app_version: str = "0.1.0"  # type: ignore
app_description: str = "test"  # type: ignore
app_debug: bool = os.getenv("APP_DEBUG", False)  # type: ignore

redis_host: str = os.getenv("REDIS_HOST", "localhost")  # type: ignore
redis_port: int = os.getenv("REDIS_PORT", 6379)  # type: ignore
cache_expire_in_seconds: int = 60 * 5  # type: ignore
redis_url: str = f"redis://{redis_host}:{redis_port}"  # type: ignore

postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")  # type: ignore
postgres_port: int = os.getenv("POSTGRES_PORT", 5432)  # type: ignore
postgres_db: str = os.getenv("POSTGRES_DB", "postgres")  # type: ignore
postgres_user: str = os.getenv("POSTGRES_USER", "postgres")  # type: ignore
postgres_password: str = os.getenv(
    "POSTGRES_PASSWORD", "postgres"
)  # type: ignore

database_url: str = (
    f"postgresql+asyncpg:"
    f"//{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/{postgres_db}"
)  # type: ignore

rabbit_host: str = os.getenv("RABBITMQ_HOST", "localhost")  # type: ignore
rabbit_port: int = os.getenv("RABBITMQ_PORT", 5672)  # type: ignore
rabit_user: str = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
rabbit_password: str = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
celery_broker_url: str = (
    f"amqp://{rabit_user}:{rabbit_password}@{rabbit_host}:{rabbit_port}//"
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
