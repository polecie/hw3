from fastapi import APIRouter, Depends
from src.services.report import get_report_service, ReportService

router = APIRouter(tags=["test"])


@router.post(
    path="/",
    summary="Заполнить базу данных тестовыми данными",
    description="Заполнить базу данных тестовыми данными",
    status_code=200,
    response_model=dict,
)
async def create_data(
    report_service: ReportService = Depends(get_report_service),
):
    return await report_service.create_data()
