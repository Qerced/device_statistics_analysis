from app.crud.base import CRUDBase
from app.models.device_user import Device


class CRUDDevice(CRUDBase):
    ...


device_crud = CRUDDevice(Device)
