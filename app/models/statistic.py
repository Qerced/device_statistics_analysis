from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey

from app.core.db import Base


class Statistic(Base):
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    device_id = Column(ForeignKey('device.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(), index=True)
