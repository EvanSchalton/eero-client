from pydantic import BaseModel
from datetime import datetime


class BurstReporters(BaseModel):
    next_burst: datetime
