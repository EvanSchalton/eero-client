from abc import abstractmethod


class SessionStorage(object):
    @property
    @abstractmethod
    def cookie(self):
        pass
