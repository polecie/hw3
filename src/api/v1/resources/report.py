import uuid

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from src.api.v1.schemas.report import (
    create_report_schema,
    get_report_schema,
    put_data_schema,
)
from src.services.report import ReportService, get_report_service

router = APIRouter()


@router.post(
    path="/",
    summary="Создать отчет",
    status_code=202,
    response_model=dict,
    responses=create_report_schema,
)
async def create_report(
    report_service: ReportService = Depends(get_report_service),
):
    """Запускает фоновую задачу celery для генераций excel-файла и возвращает
    ее **id**."""
    return await report_service.create()


@router.get(
    path="/{report_id}",
    summary="Получить отчет",
    status_code=200,
    responses=get_report_schema,
    response_class=FileResponse,
)
async def get_report(report_id: uuid.UUID, report_service: ReportService = Depends(get_report_service)):
    """Возвращает результат задачи в виде ссылки на скачивание excel-файла.

    Отчет можно получить только один раз. При необходимости следует
    сгенерировать отчет еще раз.
    """
    return await report_service.get(report_id)


@router.get(
    path="/",
    summary="Заполнить базу данных тестовыми данными",
    status_code=200,
    response_model=dict,
    responses=put_data_schema,
)
async def create_data(
    report_service: ReportService = Depends(get_report_service),
):
    """Заполняет базу тестовыми данным.

    Тестовые данные **генерируются рандомно**, с условием, что всегда
    имеется одно меню, для того чтобы excel-отчет не был пустым.
    """
    return await report_service.put()
