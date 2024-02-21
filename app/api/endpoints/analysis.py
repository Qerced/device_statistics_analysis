from http import HTTPStatus

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_exists
from app.celery.tasks import prepare_analysis
from app.core.db import get_async_session
from app.crud import device_crud, user_crud
from app.schemas.analysis import AnalysisDb, AnalysisFilter

router = APIRouter()


NOT_FOUND = 'Analysis not found, try again later.'


@router.post('/create')
async def create_analysis(
    filter: AnalysisFilter,
    session: AsyncSession = Depends(get_async_session)
):
    if filter.device_id:
        await check_exists(
            session, filter.device_id, device_crud, raise_if_exists=False
        )
    if filter.user_id:
        await check_exists(
            session, filter.user_id, user_crud, raise_if_exists=False
        )
    return JSONResponse({'task_id': prepare_analysis.delay(
        filter.device_id,
        filter.user_id,
        filter.period.dict() if filter.period else None
    ).id})


@router.get('/get_result/{task_id}', response_model=AnalysisDb)
async def get_analysis_result(task_id: str):
    result = AsyncResult(task_id)
    if result.ready():
        return result.get()
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=NOT_FOUND
    )
