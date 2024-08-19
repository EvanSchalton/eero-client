from ...session import SessionStorage
from ..api_client import APIClient
from ..models.account import Account
from ..routes.method_factory import make_method
from ..routes.routes import GET_RESOURCES
from .eero_auth_handler import EeroAuthHandler
from .network import NetworkClient


class Eero(EeroAuthHandler):
    def __init__(self, session: SessionStorage) -> None:
        self.session = session
        self.client = APIClient()
        self._network_clients: dict[str, NetworkClient] | None = None

    @property
    def network_clients(self) -> dict[str, NetworkClient]:
        if self._network_clients is None:
            if not self.is_authenticated:
                raise ValueError("Not authenticated")
            self._network_clients = {
                i.name: NetworkClient(
                    network_info=i,
                    session=self.session,
                    client=self.client,
                    **i.model_dump(),
                )
                for i in self.account.networks.data
            }

        return self._network_clients

    @network_clients.setter
    def network_clients(
        self, network_clients: dict[str, NetworkClient]
    ):
        self._network_clients = network_clients

    @property
    def account(self) -> Account:
        # return Account.model_validate(self.client.get("account", cookies=self._cookie_dict))
        return make_method(
            method="get",
            action="account",
            resource=GET_RESOURCES["account"],
        )(self)
