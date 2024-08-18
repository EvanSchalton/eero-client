# bump_version.py

import re

VERSIONFILE = "eero/version.py"
with open(VERSIONFILE, "r") as vf:
    verstr = vf.read()

VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstr, re.M)

if mo:
    verstr = mo.group(1)
    raw_version = tuple(map(int, verstr.split(".")))
    version_list = list(raw_version)
    if len(version_list) == 2:
        version_list.append(0)  # default to 0 for patch version

    if len(version_list) != 3:
        raise RuntimeError(f"Unable to parse version string: {verstr}")

    major, minor, patch = version_list
    if len(raw_version) == 3:
        patch += 1  # Increment patch version for non major.minor versions
    new_version = f"{major}.{minor}.{patch}"

    with open(VERSIONFILE, "w") as vf:
        vf.write(f"__version__ = '{new_version}'\n")

    print(f"Bumped version to {new_version}")
else:
    raise RuntimeError("Unable to find version string in version.py.")
