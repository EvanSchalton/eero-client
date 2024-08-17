from pydantic import BaseModel
from http import HTTPStatus
from datetime import datetime


class Error(BaseModel):
    code: HTTPStatus
    server_time: datetime
    error: str


class ErrorMeta(BaseModel):
    meta: Error
