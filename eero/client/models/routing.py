from pydantic import BaseModel

from .device import RoutingDeviceData
from .forward import Forward
from .reservation import Reservation


class RoutingDevices(BaseModel):
    url: str
    data: list[RoutingDeviceData]


class RoutingReservations(BaseModel):
    url: str
    data: list[Reservation]


class RoutingForwards(BaseModel):
    url: str
    data: list[Forward]


class RoutingPinholes(BaseModel):
    url: str
    data: list[dict[str, str]]  # TODO: Create Pinhole model


class Routing(BaseModel):
    url: str
    devices: RoutingDevices
    reservations: RoutingReservations
    forwards: RoutingForwards
    pinholes: RoutingPinholes
