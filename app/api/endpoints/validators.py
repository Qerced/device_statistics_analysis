from http import HTTPStatus
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Device, Statistic, User

ALREADY_EXISTS = 'Object with this id already exists.'
NOT_FOUND = 'No such object found in the database.'


async def check_exists(
    session: AsyncSession,
    id: int,
    crud: CRUDBase,
    raise_if_exists: bool = True
) -> Optional[Union[Device, Statistic, User]]:
    if instance := await crud.get(session, id):
        if raise_if_exists:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=ALREADY_EXISTS
            )
        return instance
    if not raise_if_exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND
        )
