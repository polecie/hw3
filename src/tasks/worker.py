from celery import Celery

from src.core import config

celery = Celery(
    "tasks",
    broker=config.celery_broker_url,
    backend="rpc://",
    include=["src.tasks.task"],
)
