from datetime import datetime

from pydantic import BaseModel


class BurstReporters(BaseModel):
    next_burst: datetime
