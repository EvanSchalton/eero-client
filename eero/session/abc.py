from abc import abstractmethod


class SessionStorage:
    @property
    @abstractmethod
    def cookie(self):
        pass
