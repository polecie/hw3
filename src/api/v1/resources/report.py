import uuid
from fastapi import APIRouter
from src.tasks.task import write_into_file

router = APIRouter(tags=["report"])


@router.post(
    path="/",
    summary="Создать отчет",
    description="Создать отчет",
    status_code=202,
    response_model=uuid.UUID,
)
async def create_report():
    write_into_file.delay()
    pass


@router.get(
    path="/{report_id}",
    summary="Получить отчет",
    description="Получить отчет",
    status_code=200,
    response_model=str,
)
async def get_report(report_id: uuid.UUID):
    pass
