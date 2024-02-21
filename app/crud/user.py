from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Device, User


class CRUDUser(CRUDBase):
    async def get(self, session: AsyncSession, id: int) -> User:
        instance = await session.execute(
            select(self.model).options(
                joinedload(self.model.devices)
            ).where(self.model.id == id)
        )
        return instance.scalars().first()

    async def add_new_device(
        self, session: AsyncSession, user: User, device: Device
    ) -> User:
        user.devices.append(device)
        return await self.update(session, user)


user_crud = CRUDUser(User)
