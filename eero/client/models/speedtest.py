from pydantic import BaseModel
from datetime import datetime

class Speedtest(BaseModel):
    up_mbps: float
    down_mbps: float
    date: datetime