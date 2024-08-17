from pydantic import BaseModel


class ThreadBorderAgent(BaseModel):
    ip: str
    port: int


class Thread(BaseModel):
    url: str
    enabled: bool
    enable_credential_syncing: bool
    name: str
    xpan_id: str
    pan_id: str
    channel: int
    master_key: str
    commissioning_credential: str
    border_agent: ThreadBorderAgent
    active_operational_dataset: str
