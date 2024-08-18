from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Capability(BaseModel):
    capable: bool
    requirements: dict[str, bool | str | None]


class UserRemediationCapability(Capability):
    capable_with_user_remediations: bool


class Capabilities(BaseModel):
    ac_compat: Capability
    device_blacklist: Capability
    device_management: Capability
    diagnostics: Capability
    led_action: Capability
    bifrost: Capability
    device_usage: Capability
    delorean: Capability
    thread_network: Capability
    thread_commissioning: Capability
    premium: Capability
    premium_payment_flow: Capability
    ad_block_viewable: Capability
    simple_setup: Capability
    ad_block: Capability
    ipv6: Capability
    ipv6_editable: Capability
    sqm: Capability
    band_steering: Capability
    acs: Capability
    dns_caching: Capability
    wpa3: Capability
    historical_insights: Capability
    per_device_insights: Capability
    historical_usage: Capability
    historical_usage_notifications: Capability
    software_end_of_life: Capability
    udp_speed_tests: Capability
    power_saving: Capability
    premium_upsell: Capability
    premium_partnerships: Capability
    premium_management: Capability
    premium_branding: Capability
    premium_isp_plan_enabled: Capability
    premium_cancel_immediately: Capability
    premium_isp_self_signup: Capability
    org_auto_associates_networks: Capability
    has_auto_trial: Capability | None = None
    can_auto_trial: Capability | None = None
    push_notification_setting_activity_report: Capability
    account_linking: Capability
    unified_content_filters: Capability
    dnsfilter_whitelists: Capability
    dnsfilter_blacklists: Capability
    dnsfilter_allowlist: Capability
    dnsfilter_blocklist: Capability
    dnsfilter_threat_categories: Capability
    ffs: Capability
    improved_profile_creation_flow: Capability
    improved_switch_networks: Capability
    smart_home_hub: Capability
    alexa_skill: Capability
    amazon_device_nickname: Capability
    new_private_devices_notifications: Capability
    ddns_enabled: Capability
    allow_block_edit: Capability
    port_forward_range: Capability
    adblock_for_profiles: Capability
    vlan: Capability
    ring_lte: Capability
    block_apps: Capability
    adblock_profile_entry: Capability
    block_apps_categories: Capability
    ownership_transfer: Capability
    is_android_web_payments: Capability
    proxied_nodes_beta_1: Capability
    proxied_nodes_beta_2: Capability
    pppoe: Capability
    backup_access_point: Capability
    thread_keychain_sharing: Capability
    post_setup_wan_troubleshooting: Capability
    eero_business_retail_upsell: Capability
    eero_business_ready: Capability
    eero_for_business_capable: Capability
    cedar: UserRemediationCapability
    homekit: UserRemediationCapability


class Flag(BaseModel):
    flag: str
    value: Any


class GeoIP(BaseModel):
    countryCode: str
    countryName: str
    city: str
    region: str
    timezone: str
    postalCode: str
    metroCode: int
    areaCode: int | None = None
    regionName: str
    isp: str
    org: str
    asn: int


class Connection(BaseModel):
    mode: str


class DHCPIP(BaseModel):
    ip: str
    mask: str
    router: str


class DHCP(BaseModel):
    mode: str
    custom: str | None = None


class Lease(BaseModel):
    mode: str
    dhcp: DHCPIP
    static: str | None = None


class IPList(BaseModel):
    ips: list[str]


class DNS(BaseModel):
    mode: str
    parent: IPList
    custom: IPList
    caching: bool


class EeroDeviceNetwork(BaseModel):
    url: str
    name: str
    created: datetime


class EeroDeviceEthernetStatusItem(BaseModel):
    interfaceNumber: int
    hasCarrier: bool
    speed: str
    isWanPort: bool
    isLte: bool
    isLeafWiredToUpstream: bool
    neighbor: str | None = None
    power_saving: bool
    original_speed: str | None = None
    derated_reason: str | None = None
    lldpInfo: list[dict[str, str]]


class EeroDeviceEthernetStatus(BaseModel):
    statuses: list[EeroDeviceEthernetStatusItem]
    wiredInternet: bool
    segmentId: str


class EeroDeviceUpdateStatus(BaseModel):
    support_expired: bool
    support_expiration_string: str
    support_expiration_date: datetime | None = None


class IP6Address(BaseModel):
    address: str
    scope: str
    interface: str


class EeroDevicePowerInfo(BaseModel):
    power_source: str
    power_source_metadata: dict[str, Any]


class EeroDevicePortDetail(BaseModel):
    ethernet_address: str
    port_name: str
    position: int


class EeroDeviceBandDetails(BaseModel):
    band: str
    ethernet_address: str


class Message(BaseModel):
    value: str


class EeroDevice(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    url: str
    resources: dict[str, str]
    serial: str
    network: EeroDeviceNetwork
    location: str
    joined: datetime
    gateway: bool
    ip_address: str
    status: str
    messages: list[Message]
    model: str
    model_number: str
    ethernet_addresses: list[str]
    ethernet_status: EeroDeviceEthernetStatus | None = None
    wifi_bssids: list[str]
    update_available: bool
    update_status: EeroDeviceUpdateStatus
    os: str
    os_version: str
    mesh_quality_bars: int | None = None
    wired: bool | None = None
    led_on: bool
    led_brightness: int
    using_wan: bool
    is_primary_node: bool
    nightlight: str | None = None
    last_reboot: datetime
    mac_address: str
    ipv6_addresses: list[IP6Address]
    organization: str | None = None
    connected_clients_count: int
    connected_wired_clients_count: int
    connected_wireless_clients_count: int
    requires_amazon_pre_authorized_code: bool
    heartbeat_ok: bool
    last_heartbeat: datetime
    connection_type: str | None = None
    power_info: EeroDevicePowerInfo
    backup_wan: str | None = None
    extended_border_agent_address: str | None = None
    provide_device_power: str | None = None
    port_details: list[EeroDevicePortDetail]
    bands: list[str]
    provides_wifi: bool
    bssids_with_bands: list[EeroDeviceBandDetails]


class EeroDevices(BaseModel):
    count: int
    data: list[EeroDevice]


class EeroDeviceClients(BaseModel):
    count: int
    url: str


class Measurement(BaseModel):
    value: float
    units: str


class Speed(BaseModel):
    status: str
    date: datetime
    up: Measurement
    down: Measurement


class Timezone(BaseModel):
    value: str
    geo_ip: str


class LastUserUpdate(BaseModel):
    last_update_started: datetime
    unresponsive_eeros: list[str]
    incomplete_eeros: list[str]


class DeviceUpdates(BaseModel):
    preferred_update_hour: int
    min_required_firmware: str
    target_firmware: str
    update_to_firmware: str
    update_required: bool
    can_update_now: bool
    has_update: bool
    update_status: str | None = None
    scheduled_update_time: datetime | None = None
    last_update_started: datetime
    last_user_update: LastUserUpdate


class InternetHealth(BaseModel):
    status: str
    isp_up: bool


class EeroNetworkHealth(BaseModel):
    status: str


class DeviceHealth(BaseModel):
    internet: InternetHealth
    eero_network: EeroNetworkHealth


class IPSettings(BaseModel):
    double_nat: bool
    public_ip: str


class DNSPolicy(BaseModel):
    block_malware: bool
    ad_block: bool


class AdBlockSettings(BaseModel):
    enabled: bool
    profiles: list[str]
    business_subnets: list[str]


class PremiumDNS(BaseModel):
    dns_policies_enabled: bool
    zscaler_location_enabled: bool
    any_policies_enabled_for_network: bool
    dns_provider: str | None = None
    dns_policies: DNSPolicy
    ad_block_settings: AdBlockSettings
    advanced_content_filters: str | None = None


class NameServers(BaseModel):
    mode: str
    custom: list[str]


class IPV6Settings(BaseModel):
    name_servers: NameServers


class GuestNetwork(BaseModel):
    url: str
    resources: dict[str, str]
    name: str
    password: str
    enabled: bool


class DDNS(BaseModel):
    enabled: bool
    subdomain: str


class RingLTE(BaseModel):
    state: str
    subscription_active: bool | None = None
    apn: str | None = None


class PremiumDetails(BaseModel):
    trial_ends: datetime | None = None
    has_payment_info: bool
    tier: str
    is_iap_customer: bool | None = None
    payment_method: str | None = None
    interval: str
    next_billing_event_date: datetime | None = None
    is_my_subscription: bool


class Networks(BaseModel):
    url: str
    resources: dict[str, str]
    capabilities: Capabilities
    flags: list[Flag]
    name: str
    display_name: str
    nickname_label: str | None = None
    password: str
    status: str
    messages: list[str]
    gateway: str
    wan_ip: str | None = None
    geo_ip: GeoIP
    gateway_ip: str | None = None
    connection: Connection
    lease: Lease
    dhcp: DHCP
    upnp: bool
    ipv6_upstream: bool
    thread: bool
    sqm: bool
    band_steering: bool
    wpa3: bool
    eeros: EeroDevices
    clients: EeroDeviceClients
    speed: Speed
    timezone: Timezone
    updates: DeviceUpdates
    health: DeviceHealth
    upstream: list[str]
    ip_settings: IPSettings
    premium_dns: PremiumDNS
    owner: str
    premium_status: str
    rebooting: str | None = None
    last_reboot: datetime
    homekit: str | None = None
    ipv6_lease: str | None = None
    ipv6: IPV6Settings
    organization: str | None = None
    image_assets: str | None = None
    access_expires_on: datetime | None = None
    guest_network: GuestNetwork
    amazon_account_linked: bool
    amazon_directed_id: str
    amazon_full_name: str
    ffs: bool
    temporary_flags: dict[str, Any]
    alexa_skill: bool
    amazon_device_nickname: bool
    vlan: str | None = None
    ddns: DDNS
    ring_lte: RingLTE
    pppoe_username: str | None = None
    pppoe_enabled: str | None = None
    proxied_nodes: str | None = None
    premium_details: PremiumDetails | None = None
    backup_internet_enabled: bool | None = None
    network_customer_type: str | None = None
    power_saving: bool | None = None
    wan_type: str | None = None
