from .abc import SessionStorage


class MemorySessionStorage(SessionStorage):
    def __init__(self, cookie: str | None = None) -> None:
        self._cookie = cookie
