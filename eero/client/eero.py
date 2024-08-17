from typing import Any, Self, NamedTuple, cast
from .client import Client
from .eero_auth_handler import EeroAuthHandler
from .models.account import Account
from pydantic import BaseModel, TypeAdapter, ValidationError
from functools import partial
from .models import (
    Networks,
    NetworkInfo,
    Device,
    ACCompat,
    Diagnostics,
    EeroDevice,
    Forward,
    GuestNetwork,
    Profile,
    Reservation,
    Speedtest,
    Updates,
    Support,
    Routing,
    Thread,
    ErrorMeta,
    BurstReporters,
)
from ..session import SessionStorage
from copy import copy
import json
import os
from logging import getLogger
from pathlib import Path

logger = getLogger("eero")

DEBUGGING_PATH = (
    Path(raw_debugging_path)
    if (raw_debugging_path := os.environ.get("DEBUGGING_PATH", None))
    else None
)
if DEBUGGING_PATH:
    DEBUGGING_PATH.mkdir(parents=True, exist_ok=True)

logger.debug("DEBUGGING_PATH: %s", DEBUGGING_PATH)


class Resource(NamedTuple):
    url: str
    model: BaseModel | None | list[BaseModel]


GET_RESOURCES: dict[str, Resource] = {
    "account": ("account", Account),
    "ac_compat": ("networks/<network_id>/ac_compat", ACCompat),
    "device_blacklist": ("networks/<network_id>/blacklist", list[Device]),
    "devices": ("networks/<network_id>/devices", list[Device]),
    "diagnostics": ("networks/<network_id>/diagnostics", Diagnostics),
    "eeros": ("networks/<network_id>/eeros", list[EeroDevice]),
    "forwards": ("networks/<network_id>/forwards", list[Forward]),
    "ouicheck": (
        "networks/<network_id>/ouicheck",
        ErrorMeta,  # TODO: Create Model (requires a subscription)
    ),
    "guestnetwork": ("networks/<network_id>/guestnetwork", GuestNetwork),
    # "password": ("networks/<network_id>/password", None),
    "profiles": ("networks/<network_id>/profiles", list[Profile]),
    "reservations": ("networks/<network_id>/reservations", list[Reservation]),
    # "settings": ("networks/<network_id>/settings", None),
    "speedtest": ("networks/<network_id>/speedtest", list[Speedtest]),
    # "transfer": ("networks/<network_id>/transfer", None),
    "updates": ("networks/<network_id>/updates", Updates),
    "support": ("networks/<network_id>/support", Support),
    "insights": (
        "networks/<network_id>/insights",
        ErrorMeta,  # TODO: Create Model (requires a subscription)
    ),
    "routing": ("networks/<network_id>/routing", Routing),
    "thread": ("networks/<network_id>/thread", Thread),
    "networks": ("networks/<network_id>", Networks),
}

POST_RESOURCES: dict[str, Resource] = {
    "burst_reporters": ("networks/<network_id>/burst_reporters", BurstReporters),
    "reboot": ("networks/<network_id>/reboot", None),
    "reboot_eero": ("eeros/<eero_id>/reboot", None),
}


def make_method(method: str, action: str, resource: Resource, **kwargs: Any):
    method = copy(method)
    action = copy(action)
    resource = copy(resource)

    logger.debug("%s: %s - %s", method, action, resource)
    # method = "get"

    # method_resources: dict[str, Resource] = GET_RESOURCES
    # if action in POST_RESOURCES:
    #     method_resources = POST_RESOURCES
    #     method = "post"

    logger.debug("%s: %s (%s)", method, action, resource)

    def func(self: Self, **kwargs: str) -> None | dict[str, Any] | BaseModel:
        url, model = resource
        logger.debug("%s: %s (%s)", action, url, model)
        for key, value in kwargs.items():
            url = url.replace("<{}>".format(key), str(value))

        result = self.refreshed(
            lambda: self.client.request(method, url, cookies=self._cookie_dict)
        )

        if model is not None:
            try:
                if DEBUGGING_PATH:
                    (DEBUGGING_PATH / f"{action}.json").write_text(
                        json.dumps(result, indent=2)
                    )

                if isinstance(result, list):
                    tpye_adatper = TypeAdapter(model)
                    return tpye_adatper.validate_python(result)
                if model == ErrorMeta:
                    logger.info(f"Not Implemented: {action} (expects error)")
                return model.model_validate(result)
            except ValidationError as e:
                if model == ErrorMeta:
                    logger.warn(f"Not Implemented: {action} (expected error)")
                    return result
                logger.error("Failed to validate %s: %s", action, e)
        return result

    return lambda self, **caller_kwargs: func(self, **kwargs, **caller_kwargs)


class APITypes:
    account: Account
    networks: Networks
    devices: list[Device]
    ac_compat: ACCompat
    device_blacklist: list[Device]
    diagnostics: Diagnostics
    eeros: list[EeroDevice]
    forwards: list[Forward]
    guestnetwork: GuestNetwork
    profiles: list[Profile]


def __network_client____init___(
    self: Self,
    session: SessionStorage,
    network_info: NetworkInfo,
    client: Client | None = None,
    **kwargs: Any,
) -> None:
    self.network_info = network_info
    self.session = session
    if client is None:
        client = Client()
    self.client = client


def create_get_method(action, resource):
    return property(
        lambda self: make_method(
            method="get",
            action=action,
            resource=resource,
            network_id=self.network_info.id,
        )(self)
    )


def create_post_method(action, resource):
    return lambda self, **kwargs: make_method(
        method="post",
        action=action,
        resource=resource,
        network_id=self.network_info.id,
    )(self, **kwargs)


# Create the methods dictionary
network_client_methods = {
    **{
        action: create_get_method(action, resource)
        for action, resource in GET_RESOURCES.items()
    },
    **{
        action: create_post_method(action, resource)
        for action, resource in POST_RESOURCES.items()
    },
}


for k, v in network_client_methods.items():
    logger.debug("%s: %s", k, v)

NetworkClient = type(
    "NetworkClient",
    (APITypes, EeroAuthHandler),
    {
        "__init__": __network_client____init___,
        "network_info": cast(NetworkInfo, None),
        "session": cast(SessionStorage, None),
        "client": cast(Client, None),
        **network_client_methods,
    },
)


class Eero(EeroAuthHandler):

    def __init__(self, session):
        self.session = session
        self.client = Client()
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
                for i in self.account().networks.data
            }

        return self._network_clients

    @network_clients.setter
    def network_clients(self, network_clients: dict[str, NetworkClient]):
        self._network_clients = network_clients

    def account(self) -> Account:
        return make_method("get", "account", GET_RESOURCES["account"])(self)
