from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_exists
from app.core.db import get_async_session
from app.crud.device import device_crud
from app.schemas.device import DeviceCreateDb

router = APIRouter()


@router.post('/create', response_model=DeviceCreateDb)
async def create_device(
    device: DeviceCreateDb, session: AsyncSession = Depends(get_async_session)
):
    await check_exists(session, device.id, device_crud)
    return await device_crud.create(session, device)
