from pydantic import BaseModel


class DeviceCreateDb(BaseModel):
    id: int
