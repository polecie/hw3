from .worker import celery


@celery.task
def write_into_file():
    return 2 + 2
