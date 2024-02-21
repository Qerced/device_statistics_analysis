from typing import Optional

from sqlalchemy import between, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from app.crud.base import CRUDBase
from app.models import Statistic, UserDevice


class CRUDStatistic(CRUDBase):
    async def get_analysis(
        self,
        session: AsyncSession,
        device_id: Optional[int] = None,
        user_id: Optional[int] = None,
        period: Optional[dict] = None
    ) -> Statistic:
        select_stmt = select([
            func.min(self.model.x).label('min_x'),
            func.min(self.model.y).label('min_y'),
            func.min(self.model.z).label('min_z'),
            func.max(self.model.x).label('max_x'),
            func.max(self.model.y).label('max_y'),
            func.max(self.model.z).label('max_z'),
            func.count().label('count'),
            func.sum(self.model.x).label('sum_x'),
            func.sum(self.model.y).label('sum_y'),
            func.sum(self.model.z).label('sum_z'),
            func.percentile_cont(0.5).within_group(
                self.model.x).label('median_x'),
            func.percentile_cont(0.5).within_group(
                self.model.y).label('median_y'),
            func.percentile_cont(0.5).within_group(
                self.model.z).label('median_z')
        ])
        if period:
            select_stmt = select_stmt.where(
                between(
                    self.model.timestamp,
                    period.get('from_analysis'),
                    period.get('to_analysis')
                )
            )
        if user_id:
            select_stmt = select_stmt.where(
                self.model.device_id.in_(
                    select(UserDevice.device_id)
                    .where(UserDevice.user_id == user_id)
                )
            )
        if device_id:
            select_stmt = select_stmt.where(
                self.model.device_id == device_id
            )
        instance = await session.execute(select_stmt)
        return instance.mappings().first()


statistic_crud = CRUDStatistic(Statistic)
