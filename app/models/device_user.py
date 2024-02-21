from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class UserDevice(Base):
    __table_args__ = (UniqueConstraint('user_id', 'device_id'),)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    device_id = Column(ForeignKey('device.id'), nullable=False)


class User(Base):
    devices = relationship(
        'Device', secondary='userdevice', back_populates='users'
    )


class Device(Base):
    users = relationship(
        'User', secondary='userdevice', back_populates='devices'
    )
