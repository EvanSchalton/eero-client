import json
import logging
import os
from pathlib import Path
from stat import S_IMODE
from types import SimpleNamespace

import pytest
from pydantic import BaseModel, field_validator

from eero.client.api_client import APIClient
from eero.client.routes import method_factory
from eero.client.routes.routes import Resource
from eero.exceptions import ClientException
from eero.session import FileSessionStorage

SECRET = "sensitive-marker-that-must-not-be-logged"


class ExpectedResponse(BaseModel):
    required_field: str


class RejectedResponse(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def reject_password(cls, value: str) -> str:
        raise ValueError(f"rejected sensitive value: {value}")


class FakeAPI:
    def __init__(self, result):
        self.client = SimpleNamespace(request=lambda method, url: result)

    @staticmethod
    def refreshed(func):
        return func()


def test_validation_failure_does_not_log_response_payload(caplog) -> None:
    caplog.set_level(logging.DEBUG, logger="eero")
    response = {"password": SECRET}

    result = method_factory.make_method(
        "get",
        "network",
        Resource("network", ExpectedResponse),
    )(FakeAPI(response))

    assert result == response
    assert SECRET not in caplog.text


def test_validator_message_does_not_log_sensitive_value(caplog) -> None:
    caplog.set_level(logging.DEBUG, logger="eero")
    response = {"password": SECRET}

    result = method_factory.make_method(
        "get",
        "network",
        Resource("network", RejectedResponse),
    )(FakeAPI(response))

    assert result == response
    assert SECRET not in caplog.text


def test_api_client_does_not_log_success_payload(caplog) -> None:
    caplog.set_level(logging.DEBUG, logger="eero")
    response = SimpleNamespace(
        text=json.dumps({"meta": {"code": 200}, "data": {"password": SECRET}})
    )

    result = APIClient()._parse_response("network", response)

    assert result == {"password": SECRET}
    assert SECRET not in caplog.text


def test_api_client_does_not_log_malformed_payload(caplog) -> None:
    caplog.set_level(logging.DEBUG, logger="eero")
    response = SimpleNamespace(text=json.dumps({"password": SECRET}))

    with pytest.raises(ClientException):
        APIClient()._parse_response("network", response)

    assert SECRET not in caplog.text


def test_debug_payload_has_owner_only_permissions(tmp_path: Path, monkeypatch) -> None:
    debug_path = tmp_path / "debug"
    monkeypatch.setattr(method_factory, "DEBUGGING_PATH", debug_path)

    method_factory._write_debug_payload("network", {"password": SECRET})

    output_path = debug_path / "network.json"
    assert json.loads(output_path.read_text()) == {"password": SECRET}
    if os.name != "nt":
        assert S_IMODE(debug_path.stat().st_mode) == 0o700
        assert S_IMODE(output_path.stat().st_mode) == 0o600


def test_file_session_storage_writes_cookie_atomically_with_owner_only_permissions(
    tmp_path: Path,
) -> None:
    cookie_path = tmp_path / "session.cookie"
    storage = FileSessionStorage(cookie_path)

    storage.cookie = SECRET

    assert isinstance(storage.cookie_file, str)
    assert cookie_path.read_text() == SECRET
    assert not list(tmp_path.glob(".session.cookie.*"))
    if os.name != "nt":
        assert S_IMODE(cookie_path.stat().st_mode) == 0o600


def test_file_session_storage_restricts_existing_cookie_permissions(
    tmp_path: Path,
) -> None:
    cookie_path = tmp_path / "session.cookie"
    cookie_path.write_text(SECRET)
    cookie_path.chmod(0o644)

    storage = FileSessionStorage(cookie_path)

    assert storage.cookie == SECRET
    if os.name != "nt":
        assert S_IMODE(cookie_path.stat().st_mode) == 0o600


def test_file_session_storage_preserves_cookie_when_atomic_replace_fails(
    tmp_path: Path, monkeypatch
) -> None:
    cookie_path = tmp_path / "session.cookie"
    cookie_path.write_text("existing-cookie")
    storage = FileSessionStorage(cookie_path)

    def fail_replace(source, destination):
        raise OSError("simulated replace failure")

    monkeypatch.setattr(os, "replace", fail_replace)

    with pytest.raises(OSError, match="simulated replace failure"):
        storage.cookie = SECRET

    assert storage.cookie == "existing-cookie"
    assert cookie_path.read_text() == "existing-cookie"
    assert not list(tmp_path.glob(".session.cookie.*"))
