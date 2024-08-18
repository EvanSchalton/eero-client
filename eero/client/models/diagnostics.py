from pydantic import BaseModel


class Diagnostics(BaseModel):
    status: str
