import asyncio
from typing import Optional

from celery import Celery

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud.statistics import statistic_crud
from app.models.statistic import Statistic

celery = Celery('tasks', broker=settings.redis_url, backend=settings.redis_url)

loop = asyncio.get_event_loop()


async def wrapper_with_session(
    device_id: Optional[int] = None,
    user_id: Optional[int] = None,
    period: Optional[dict] = None
):
    async with AsyncSessionLocal() as session:
        return await statistic_crud.get_analysis(
            session, device_id, user_id, period
        )


@celery.task
def prepare_analysis(
    device_id: Optional[int] = None,
    user_id: Optional[int] = None,
    period: Optional[dict] = None
) -> Statistic:
    return dict(loop.run_until_complete(
        wrapper_with_session(device_id, user_id, period)
    ))
