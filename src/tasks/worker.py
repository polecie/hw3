from celery import Celery

from src.core.config import config

celery = Celery(
    "tasks",
    broker=config.celery_broker_url,
    backend=config.celery_backend_url,
    include=["src.tasks.task"],
)
