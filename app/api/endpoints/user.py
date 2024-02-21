from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_exists
from app.core.db import get_async_session
from app.crud.device import device_crud
from app.crud.user import user_crud
from app.schemas.user import UserCreateDb, UserDeviceCreate, UserDeviceDb

router = APIRouter()


@router.post('/create', response_model=UserCreateDb)
async def create_user(
    user: UserCreateDb, session: AsyncSession = Depends(get_async_session)
):
    await check_exists(session, user.id, user_crud)
    return await user_crud.create(session, user)


@router.post('/add_device', response_model=UserDeviceDb)
async def add_device(
    user_device: UserDeviceCreate,
    session: AsyncSession = Depends(get_async_session)
):
    user = await check_exists(
        session, user_device.user_id, user_crud, raise_if_exists=False
    )
    device = await check_exists(
        session, user_device.device_id, device_crud, raise_if_exists=False
    )
    return await user_crud.add_new_device(session, user, device)
