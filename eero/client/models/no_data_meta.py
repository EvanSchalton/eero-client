from datetime import datetime
from http import HTTPStatus

from pydantic import BaseModel


class NoData(BaseModel):
    code: HTTPStatus
    server_time: datetime


class NoDataMeta(BaseModel):
    meta: NoData
