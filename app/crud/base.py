from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Device, Statistic, User
from app.schemas import DeviceCreateDb, StatisticsCreate, UserCreateDb


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self, session: AsyncSession, id: int
    ) -> Union[Device, Statistic, User]:
        instance = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return instance.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        schema: Union[DeviceCreateDb, StatisticsCreate, UserCreateDb]
    ) -> Union[Device, Statistic, User]:
        instance = self.model(**schema.dict())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(
        self, session: AsyncSession, instance: Union[Device, Statistic, User]
    ) -> Union[Device, Statistic, User]:
        await session.merge(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
