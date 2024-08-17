from pydantic import BaseModel
from datetime import datetime

class Phone(BaseModel):
    value: str
    country_code: str
    national_number: str
    verified: bool

class Email(BaseModel):
    value: str
    verified: bool

class NetworkInfo(BaseModel):
    url: str
    name: str
    created: str
    nickname_label: str | None = None 
    access_expires_on: datetime | None = None 
    amazon_directed_id: str

    @property
    def id(self):
        return self.url.split('/')[-1]

class Networks(BaseModel):
    count: int
    data: list[NetworkInfo]

class Auth(BaseModel):
    type: str
    provider_id: str | None = None 
    service_id: str | None = None 

class PremiumDetails(BaseModel):
    trial_ends: datetime | None = None 
    has_payment_info: bool
    tier: str
    is_iap_customer: bool
    payment_method: str | None = None 
    interval: str
    next_billing_event_date: datetime | None = None 

class PushSettings(BaseModel):
    networkOffline: bool
    nodeOffline: bool

class Consent(BaseModel):
    consented: bool

class Consents(BaseModel):
    marketing_emails: Consent

class Account(BaseModel):
    name: str
    phone: Phone
    email: Email
    log_id: str
    organization_id: str | None = None 
    image_assets: list[str] | None = None 
    networks: Networks
    auth: Auth
    role: str | None = None 
    is_beta_bug_reporter_eligible: bool
    can_transfer: bool
    is_premium_capable: bool
    payment_failed: bool
    premium_status: str
    premium_details: PremiumDetails
    push_settings: PushSettings
    trust_certificates_etag: str
    consents: Consents
    can_migrate_to_amazon_login: bool
    eero_for_business: bool
    mdu_program: bool
    business_details: str | None = None 


    