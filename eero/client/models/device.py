from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceSource(BaseModel):
    location: str | None = None
    is_gateway: bool | None = None
    model: str | None = None
    display_name: str | None = None
    serial_number: str | None = None
    is_proxied_node: bool | None = None
    url: str | None = None


class RateInfo(BaseModel):
    rate_bps: int | str | None = None
    mcs: int | str | None = None
    nss: int | str | None = None
    guard_interval: str | None = None
    channel_width: str | None = None
    phy_type: str | None = None


class DeviceEthernetStatus(BaseModel):
    has_carrier: bool
    interface_number: int
    speed: str
    is_wan_port: bool
    is_lte: bool
    port_name: str


class DeviceConnectivity(BaseModel):
    rx_bitrate: str | None = None
    signal: str | None = None
    signal_avg: str | None = None
    score: float | None = None
    score_bars: int | None = None
    frequency: int | None = None
    rx_rate_info: RateInfo | None = None
    tx_rate_info: RateInfo | None = None
    ethernet_status: DeviceEthernetStatus | None = None


class Interface(BaseModel):
    frequency: str | None = None
    frequency_unit: str | None = None


class Profile(BaseModel):
    url: str
    name: str
    paused: bool


class HomeKit(BaseModel):
    registered: bool
    protection_mode: str


class DeviceRingLTE(BaseModel):
    is_not_pausable: bool
    ring_managed: bool
    lte_enabled: bool


class AmazonDevicesDetail(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_name_internal: str | None = None


class RoutingDeviceData(BaseModel):
    url: str
    mac: str
    nickname: str | None = None


class ProfileDevice(RoutingDeviceData):
    model_config = ConfigDict(protected_namespaces=())
    manufacturer: str | None = None
    manufacturer_device_type_id: str | None = None
    ip: str | None = None
    ips: list[str]
    hostname: str | None = None
    connected: bool
    wireless: bool
    connection_type: str | None = None
    source: DeviceSource
    last_active: datetime | None = None
    first_active: datetime | None = None
    connectivity: DeviceConnectivity
    interface: Interface
    usage: str | None = None
    homekit: HomeKit | None = None
    device_type: str
    auth: str | None = None
    paused: bool
    display_name: str | None = None
    is_private: bool
    model_name: str | None = None


class Device(ProfileDevice):
    eui64: str
    ipv6_addresses: list[str]
    profile: Profile | None = None
    blacklisted: bool | None = None
    is_guest: bool
    channel: int | None = None
    secondary_wan_deny_access: bool
    ring_lte: DeviceRingLTE
    ipv4: str | None = None
    is_proxied_node: bool
    amazon_devices_detail: AmazonDevicesDetail | None = None
    ssid: str | None = None
    subnet_kind: str | None = None
