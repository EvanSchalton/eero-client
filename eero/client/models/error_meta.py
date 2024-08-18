from datetime import datetime
from http import HTTPStatus

from pydantic import BaseModel


class Error(BaseModel):
    code: HTTPStatus
    server_time: datetime
    error: str


class ErrorMeta(BaseModel):
    meta: Error
