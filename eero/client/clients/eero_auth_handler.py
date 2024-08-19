from ...exceptions import ClientException
from ...session import SessionStorage
from ..api_client import APIClient


class EeroAuthHandler:
    def __init__(self, session: SessionStorage):
        self.session = session
        self.client = APIClient()

    @property
    def _cookie_dict(self):
        if not self.is_authenticated:
            return dict()
        else:
            return dict(s=self.session.cookie)

    @property
    def is_authenticated(self) -> bool:
        return self.session.cookie is not None

    def login(self, identifier):
        # type(string) -> string
        json = dict(login=identifier)
        data = self.client.post("login", json=json)
        return data["user_token"]

    def login_verify(self, verification_code, user_token):
        response = self.client.post(
            "login/verify",
            json=dict(code=verification_code),
            cookies=dict(s=user_token),
        )
        self.session.cookie = user_token
        return response

    def refreshed(self, func):
        try:
            return func()
        except ClientException as exception:
            if (
                exception.status == 401
                and exception.error_message == "error.session.refresh"
            ):
                self.login_refresh()
                return func()
            else:
                raise

    def login_refresh(self):
        response = self.client.post("login/refresh", cookies=self._cookie_dict)
        self.session.cookie = response["user_token"]
