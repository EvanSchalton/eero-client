import os
import tempfile
from pathlib import Path

from .abc import SessionStorage


class FileSessionStorage(SessionStorage):
    def __init__(self, cookie_file: str | os.PathLike[str]) -> None:
        self.cookie_file = os.path.abspath(cookie_file)
        self._cookie_path = Path(self.cookie_file)
        self.__cookie: str | None

        try:
            self.__cookie = self._cookie_path.read_text()
            if os.name != "nt":
                self._cookie_path.chmod(0o600)
        except OSError:
            self.__cookie = None

    @property
    def cookie(self) -> str | None:
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie: str) -> None:
        file_descriptor, temporary_path = tempfile.mkstemp(
            dir=self._cookie_path.parent,
            prefix=f".{self._cookie_path.name}.",
            text=True,
        )
        try:
            if os.name != "nt":
                os.fchmod(file_descriptor, 0o600)
            with os.fdopen(file_descriptor, "w") as cookie_file:
                cookie_file.write(cookie)
            os.replace(temporary_path, self._cookie_path)
            if os.name != "nt":
                self._cookie_path.chmod(0o600)
            self.__cookie = cookie
        except OSError:
            try:
                os.close(file_descriptor)
            except OSError:
                pass
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
            raise
