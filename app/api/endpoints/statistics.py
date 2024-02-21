from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_exists
from app.core.db import get_async_session
from app.crud import statistic_crud, device_crud
from app.schemas.statistics import StatisticsCreate, StatisticsDb

router = APIRouter()


@router.post('/create', response_model=StatisticsDb)
async def create_statistic(
    statistics: StatisticsCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_exists(
        session, statistics.device_id, device_crud, raise_if_exists=False
    )
    return await statistic_crud.create(session, statistics)
