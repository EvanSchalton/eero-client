from datetime import datetime

from pydantic import BaseModel


class Speedtest(BaseModel):
    up_mbps: float
    down_mbps: float
    date: datetime
