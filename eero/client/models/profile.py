from pydantic import BaseModel

from .device import ProfileDevice


class ProfileState(BaseModel):
    value: str
    schedule: str | None  # TODO: Likely a dict


class DNSPolicies(BaseModel):
    block_poronographic_content: bool | None = None
    block_illegal_content: bool
    block_violent_content: bool
    safe_search_enabled: bool


class AdvancedContentFilters(BaseModel):
    blocked_list: list[str]
    allowed_list: list[str]


class AdBlockSettings(BaseModel):
    enabled: bool
    enabled_for_network: bool


class PremiumDNS(BaseModel):
    zscaler_location_enabled: bool
    dns_provider: str | None = None
    dns_policies: DNSPolicies
    advanced_content_filters: AdvancedContentFilters
    ad_block_settings: AdBlockSettings
    blocked_applications: list[str]


class UnifiedContentFilters(BaseModel):
    is_content_filters_set: bool
    dns_policies: dict[str, bool]


class Profile(BaseModel):
    url: str
    resources: dict[str, str]
    name: str
    paused: bool
    devices: list[ProfileDevice]
    state: ProfileState
    premium_dns: PremiumDNS
    unified_content_filters: UnifiedContentFilters
    proxied_nodes: list[str]
