from typing import NamedTuple

from pydantic import BaseModel, TypeAdapter

from ..models import (
    ACCompat,
    Account,
    BurstReporters,
    Device,
    Diagnostics,
    EeroDevice,
    ErrorMeta,
    Forward,
    GuestNetwork,
    Networks,
    NoDataMeta,
    Profile,
    Reservation,
    Routing,
    Speedtest,
    Support,
    Thread,
    Updates,
)


class Resource(NamedTuple):
    url: str
    model: type[BaseModel] | type[TypeAdapter] | None


GET_RESOURCES: dict[str, Resource] = {
    "account": Resource("account", Account),
    "ac_compat": Resource("networks/<network_id>/ac_compat", ACCompat),
    "device_blacklist": Resource(
        "networks/<network_id>/blacklist", TypeAdapter[list[Device]]
    ),
    "devices": Resource("networks/<network_id>/devices", TypeAdapter[list[Device]]),
    "diagnostics": Resource("networks/<network_id>/diagnostics", Diagnostics),
    "eeros": Resource("networks/<network_id>/eeros", TypeAdapter[list[EeroDevice]]),
    "forwards": Resource("networks/<network_id>/forwards", TypeAdapter[list[Forward]]),
    "ouicheck": Resource(
        "networks/<network_id>/ouicheck",
        ErrorMeta,  # TODO: Create Model (requires a subscription)
    ),
    "guestnetwork": Resource("networks/<network_id>/guestnetwork", GuestNetwork),
    # "password": Resource("networks/<network_id>/password", None),
    "profiles": Resource("networks/<network_id>/profiles", TypeAdapter[list[Profile]]),
    "reservations": Resource(
        "networks/<network_id>/reservations", TypeAdapter[list[Reservation]]
    ),
    # "settings": Resource("networks/<network_id>/settings", None),
    "speedtest": Resource(
        "networks/<network_id>/speedtest", TypeAdapter[list[Speedtest]]
    ),
    # "transfer": Resource("networks/<network_id>/transfer", None),
    "updates": Resource("networks/<network_id>/updates", Updates),
    "support": Resource("networks/<network_id>/support", Support),
    "insights": Resource(
        "networks/<network_id>/insights",
        ErrorMeta,  # TODO: Create Model (requires a subscription)
    ),
    "routing": Resource("networks/<network_id>/routing", Routing),
    "thread": Resource("networks/<network_id>/thread", Thread),
    "networks": Resource("networks/<network_id>", Networks),
}

POST_RESOURCES: dict[str, Resource] = {
    "burst_reporters": Resource(
        "networks/<network_id>/burst_reporters", BurstReporters
    ),
    "reboot": Resource("networks/<network_id>/reboot", None),
    "reboot_eero": Resource("eeros/<eero_id>/reboot", None),
    "run_speedtest": Resource("networks/<network_id>/speedtest", NoDataMeta),
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
