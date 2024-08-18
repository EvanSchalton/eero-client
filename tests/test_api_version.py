from eero.version import __version__
from eero.client.api_client import API_VERSION


def get_version(version_str: str) -> tuple[int, int, int | None]:
    # Sometimes the version will only be major.minor other times it'll be major.minor.patch
    version = list(map(int, version_str.split(".")))
    if len(version) == 2:
        version.append(None)

    return tuple(version)


def test_version_matches_api_version() -> None:
    package_version = get_version(__version__)
    api_version = get_version(API_VERSION)

    assert package_version[0] == api_version[0]
    assert package_version[1] == api_version[1]
    assert package_version[2] == api_version[2] or api_version[2] is None
