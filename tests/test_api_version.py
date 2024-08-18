from eero.client.api_client import API_VERSION
from eero.version import __version__


def get_version(version_str: str) -> tuple[int, int, int | None]:
    # Sometimes the version will only be major.minor other times it'll be major.minor.patch
    version: list[int] = list(map(int, version_str.split(".")))
    major: int = version[0]
    minor: int = version[1]
    patch: int | None = version[2] if len(version) == 3 else None

    return major, minor, patch


def test_version_matches_api_version() -> None:
    package_version = get_version(__version__)
    api_version = get_version(API_VERSION)

    assert package_version[0] == api_version[0]
    assert package_version[1] == api_version[1]
    assert package_version[2] == api_version[2] or api_version[2] is None
