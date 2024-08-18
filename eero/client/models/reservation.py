from pydantic import BaseModel


class Reservation(BaseModel):
    url: str
    device: str
    mac: str
    description: str
    ip: str
