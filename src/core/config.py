from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# application settings
app_name: str = "restapi"
app_version: str = "0.1.0"
app_description: str = "asynchronous restapi for restaurant menu featured with crud operations for dish, submenu, menu"
app_debug: bool = os.getenv("APP_DEBUG", True)  # type: ignore

# redis settings
redis_host: str = os.getenv("REDIS_HOST", "localhost")
redis_port: int = os.getenv("REDIS_PORT", 6379)  # type: ignore
cache_expire_in_seconds: int = os.getenv(
    "CACHE_EXPIRE_IN_SECONDS", 60 * 5
)  # type: ignore
redis_url: str = f"redis://{redis_host}:{redis_port}"

# postgres settings
postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
postgres_port: int = os.getenv("POSTGRES_PORT", 5432)  # type: ignore
postgres_db: str = os.getenv("POSTGRES_DB", "postgres")
postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
database_url: str = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

test_pgdb_host: str = os.getenv("TEST_DB_HOST", "localhost")
test_pgdb_port: int = os.getenv("TEST_DB_PORT", 5432)  # type: ignore
test_pgdb_user: str = os.getenv("TEST_DB_USER", "ylab")
test_pgdb_password: str = os.getenv("TEST_DB_PASSWORD", "ylab")
test_pgdb_db: str = os.getenv("TEST_DB", "ylab")
test_pgdb_url: str = f"postgresql+asyncpg://{test_pgdb_user}:{test_pgdb_password}@{test_pgdb_host}:{test_pgdb_port}/{test_pgdb_db}"

test_redis_host: str = os.getenv("TEST_REDIS_HOST", "localhost")
test_redis_port: str = os.getenv("TEST_REDIS_PORT", 6379)  # type: ignore
test_redis_url: str = f"redis://{test_redis_host}:{test_redis_port}"

BASE_DIR = Path(__file__).resolve().parent.parent
