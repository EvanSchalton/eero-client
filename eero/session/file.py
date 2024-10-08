from .abc import SessionStorage


class FileSessionStorage(SessionStorage):
    def __init__(self, cookie_file):
        from os import path

        self.cookie_file = path.abspath(cookie_file)

        try:
            with open(self.cookie_file, "r") as f:
                self.__cookie = f.read()
        except IOError:
            self.__cookie = None

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open(self.cookie_file, "w+") as f:
            f.write(self.__cookie)
