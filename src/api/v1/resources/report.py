import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from src.api.v1.schemas.report import data_schema, report_schema
from src.services.report import ReportService, get_report_service
from src.tasks.task import save_menu

router = APIRouter(tags=["report"])


@router.post(
    path="/",
    summary="Создать отчет",
    description="Создать отчет",
    status_code=202,
    response_model=dict,
    responses=report_schema,
)
async def create_report(
    report_service: ReportService = Depends(get_report_service),
):
    """Запускает фоновую задачу celery для генераций excel-файла и возвращает
    ее id.

    :param report_service: Сервис для работы с логикой.
    """
    menu: str = await report_service.get()
    response: AsyncResult = save_menu.delay(menu)
    if response:
        return {"id": response.id}


@router.get(
    path="/{report_id}",
    summary="Получить отчет",
    description="Получить отчет",
    status_code=200,
    response_model=dict,
    response_class=FileResponse,
)
async def get_report(task_id: uuid.UUID):
    """Возвращает результат задачи в виде ссылки на скачивание excel-файла.

    :param task_id: Идентификатор задачи.
    """
    report_name = AsyncResult(str(task_id), app=save_menu)
    report: str = report_name.get()
    return FileResponse(path=f"{report}", filename=report, media_type="multipart/form-data")


@router.get(
    path="/",
    summary="Заполнить базу данных тестовыми данными",
    description="Заполнить базу данных тестовыми данными",
    status_code=200,
    response_model=dict,
    responses=data_schema,
)
async def create_data(
    report_service: ReportService = Depends(get_report_service),
):
    """Заполняет базу тестовыми данными, для последующей генераций меню в
    excel-файл.

    :param report_service: Сервис для работы с логикой.
    """
    return await report_service.put()
