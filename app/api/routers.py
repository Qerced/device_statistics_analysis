from fastapi import APIRouter

from app.api.endpoints import (
    analysis_router, device_router, statistics_router, user_router
)

main_router = APIRouter()
main_router.include_router(
    analysis_router, prefix='/analysis',  tags=['Analysis']
)
main_router.include_router(device_router, prefix='/device', tags=['Device'])
main_router.include_router(
    statistics_router, prefix='/statistic', tags=['Statistics']
)
main_router.include_router(user_router, prefix='/user', tags=['User'])
