from datetime import datetime

from pydantic import BaseModel


class StatisticsCreate(BaseModel):
    x: float
    y: float
    z: float
    device_id: int


class StatisticsDb(StatisticsCreate):
    timestamp: datetime
