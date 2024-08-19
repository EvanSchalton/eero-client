from ...exceptions import ClientException
from ...session import MemorySessionStorage, SessionStorage
from ..api_client import APIClient


class EeroAuthHandler:
    def __init__(
        self,
        session: SessionStorage | None = None,
        client: APIClient | None = None,
    ):
        if session is None:
            session = MemorySessionStorage()
        if client is None:
            client = APIClient(session_cookie=session.cookie)

        self.session = session
        self.client = client

    def _pass_cookie(self):
        self.client.session_cookie = self.session.cookie

    @property
    def is_authenticated(self) -> bool:
        if self.session.cookie is not None:
            if self.client.session_cookie is None:
                self._pass_cookie()
            return True
        return False

    def login(self, identifier):
        # type(string) -> string
        json = dict(login=identifier)
        data = self.client.post("login", json=json)
        return data["user_token"]

    def login_verify(self, verification_code, user_token):
        self.session.cookie = user_token
        self._pass_cookie()
        response = self.client.post(
            "login/verify",
            json=dict(code=verification_code),
        )
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
        response = self.client.post("login/refresh")
        self.session.cookie = response["user_token"]
        self._pass_cookie()
