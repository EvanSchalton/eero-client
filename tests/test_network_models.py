from datetime import datetime

from pydantic import TypeAdapter

from eero.client.models.networks import NetworkHomeKit


def test_network_homekit_accepts_structured_api_response() -> None:
    adapter: TypeAdapter[NetworkHomeKit | str | None] = TypeAdapter(
        NetworkHomeKit | str | None
    )

    result = adapter.validate_python(
        {
            "enabled": True,
            "enabledLastChanged": "2026-07-30T23:47:00Z",
            "managedNetworkEnabled": False,
        }
    )

    assert isinstance(result, NetworkHomeKit)
    assert result.enabled is True
    assert isinstance(result.enabledLastChanged, datetime)
    assert result.managedNetworkEnabled is False


def test_network_homekit_accepts_legacy_forms() -> None:
    adapter: TypeAdapter[NetworkHomeKit | str | None] = TypeAdapter(
        NetworkHomeKit | str | None
    )

    assert adapter.validate_python(None) is None
    assert adapter.validate_python("enabled") == "enabled"
