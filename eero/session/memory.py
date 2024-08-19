from .abc import SessionStorage


class MemorySessionStorage(SessionStorage):
    def __init__(self, cookie: str | None = None) -> None:
        self._cookie = cookie

    @property
    def cookie(self) -> str | None:
        return self._cookie

    @cookie.setter
    def cookie(self, cookie: str | None) -> None:
        self._cookie = cookie
        return
