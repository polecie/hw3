from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.mixin import Service
from src.db.db import get_async_session


class ReportService(Service):
    async def create_data(self):
        # statement = ""
        status = False
        async with self.session as session:
            async with session.begin():
                try:
                    # response = await session.execute()
                    status = True
                except Exception:
                    pass
        if status is True:
            return {"status": status, "message": "The data has been added"}
        return {"status": status, "message": "Bad request"}


async def get_report_service(
    session: AsyncSession = Depends(get_async_session),
) -> ReportService:
    return ReportService(session=session)
