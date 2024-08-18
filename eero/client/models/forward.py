from pydantic import BaseModel


class Forward(BaseModel):
    url: str
    ip: str
    description: str
    gateway_port: int
    client_port: int
    protocol: str
    enabled: bool
    reservation: str
