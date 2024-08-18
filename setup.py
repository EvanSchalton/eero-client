import os.path
import re

from setuptools import find_packages, setup

VERSIONFILE = "eero/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

README_FILE = next(
    r for r in ["./README.md", "./README.txt", "./README"] if os.path.isfile(r)
)

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="eero-client",
    version=verstr,
    description="Manage eero network devices",
    long_description=open(README_FILE, "r").read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="eero",
    author="Evan Schalton",
    author_email="Evan.Schalton@Gmail.com",
    url="https://github.com/EvanSchalton/eero-client",
    license="MIT License",
    packages=find_packages(exclude=["ez_setup", "example", "tests", "external"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.10",  # Require Python 3.10 or newer
    package_data={"eero": ["py.typed"]},  # Include the py.typed file
)
