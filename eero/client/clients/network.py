import os
from logging import getLogger
from pathlib import Path
from typing import Any, Self, cast
from ...session import SessionStorage
from ..api_client import APIClient
from .eero_auth_handler import EeroAuthHandler
from ..models import NetworkInfo
from ..routes import (
    APITypes,
    network_client_methods,
)


def __network_client____init___(
    self: Self,
    session: SessionStorage,
    network_info: NetworkInfo,
    client: APIClient | None = None,
    **kwargs: Any,
) -> None:
    self.network_info = network_info
    self.session = session
    if client is None:
        client = APIClient()
    self.client = client


NetworkClient = type(
    "NetworkClient",
    (APITypes, EeroAuthHandler),
    {
        "__init__": __network_client____init___,
        "network_info": cast(NetworkInfo, None),
        "session": cast(SessionStorage, None),
        "client": cast(APIClient, None),
        **network_client_methods,
    },
)
