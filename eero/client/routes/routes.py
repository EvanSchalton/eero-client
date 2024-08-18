from typing import NamedTuple
from pydantic import BaseModel

from ..models import (
    ACCompat,
    BurstReporters,
    Device,
    Diagnostics,
    EeroDevice,
    ErrorMeta,
    Forward,
    GuestNetwork,
    Networks,
    Profile,
    Reservation,
    Routing,
    Speedtest,
    Support,
    Thread,
    Updates,
    Account,
    NoDataMeta,
)


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
    "run_speedtest": ("networks/<network_id>/speedtest", NoDataMeta),
}


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
    reservations: list[Reservation]
    speedtest: list[Speedtest]
    updates: Updates
    support: Support
    routing: Routing
    thread: Thread
    burst_reporters: BurstReporters
    insights: ErrorMeta
    ouicheck: ErrorMeta
