import uuid

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from src.api.v1.schemas.report import (
    create_report_schema,
    get_report_schema,
    put_data_schema,
)
from src.services.report import ReportService, get_report_service

router = APIRouter(tags=["report"])


@router.post(
    path="/",
    summary="Создать отчет",
    description="Создать отчет",
    status_code=202,
    response_model=dict,
    responses=create_report_schema,
)
async def create_report(
    report_service: ReportService = Depends(get_report_service),
):
    """Запускает фоновую задачу celery для генераций excel-файла и возвращает
    ее id.

    :param report_service: Сервис для работы с логикой.
    """
    return await report_service.create()


@router.get(
    path="/{report_id}",
    summary="Получить отчет",
    description="Получить отчет",
    status_code=200,
    # response_model=dict,
    responses=get_report_schema,
    response_class=FileResponse,
)
async def get_report(report_id: uuid.UUID, report_service: ReportService = Depends(get_report_service)):
    """Возвращает результат задачи в виде ссылки на скачивание excel-файла.

    :param report_id: Идентификатор задачи.
    :param report_service: Сервис для работы с логикой.
    """
    return await report_service.get(report_id)


@router.get(
    path="/",
    summary="Заполнить базу данных тестовыми данными",
    description="Заполнить базу данных тестовыми данными",
    status_code=200,
    response_model=dict,
    responses=put_data_schema,
)
async def create_data(
    report_service: ReportService = Depends(get_report_service),
):
    """Заполняет базу тестовыми данными, для последующей генераций меню в
    excel-файл.

    :param report_service: Сервис для работы с логикой.
    """
    return await report_service.put()
