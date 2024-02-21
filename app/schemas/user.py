from pydantic import BaseModel

from app.schemas.device import DeviceCreateDb


class UserCreateDb(BaseModel):
    id: int


class UserDeviceCreate(BaseModel):
    user_id: int
    device_id: int


class UserDeviceDb(UserCreateDb):
    devices: list[DeviceCreateDb]
