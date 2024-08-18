from typing import Any

from pydantic import BaseModel


class LastUserUpdate(BaseModel):
    last_update_started: str
    unresponsive_eeros: list[Any]  # TODO: Update
    incomplete_eeros: list[Any]  # TODO: Update


class Updates(BaseModel):
    preferred_update_hour: int
    min_required_firmware: str
    target_firmware: str
    update_to_firmware: str
    update_required: bool
    can_update_now: bool
    has_update: bool
    update_status: Any | None  # TODO: Update
    scheduled_update_time: Any | None  # TODO: Update
    last_update_started: str
    last_user_update: LastUserUpdate
    manifest_resource: str
