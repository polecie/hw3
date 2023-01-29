app_name = "restapi"
app_version = "0.1.0"
app_description = "async"
app_host = "127.0.0.1"
app_port = 8000
app_debug = True

redis_host = "localhost"
redis_port = 6379
cache_expire_in_seconds: int = 1500

database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"