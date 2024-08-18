import re

from invoke import task


@task
def install_dependencies(c):
    """Install project dependencies."""
    c.run("pip install -r requirements.txt")


@task
def install_dev_dependencies(c):
    """Install development dependencies."""
    c.run("pip install -r requirements-dev.txt")


@task
def check_format(c):
    """Run isort and black for code formatting."""
    c.run("isort . --check --diff")
    c.run("black . --check --diff")


@task
def format(c):
    """Run isort and black for code formatting."""
    c.run("isort .")
    c.run("black .")


@task
def lint(c):
    """Run ruff to check for linting and style issues."""
    c.run("ruff check . --fix")


@task
def check_lint(c):
    """Run ruff to check for linting and style issues."""
    c.run("ruff check .")


@task
def check_type(c):
    """Run mypy to check type annotations."""
    c.run("mypy .")


@task
def test(c):
    """Run pytest to execute tests."""
    c.run("pytest")


@task
def build(c):
    """Build the Python package."""
    c.run("pip install wheel")  # Ensure wheel is installed
    c.run("python setup.py sdist bdist_wheel")


@task
def publish(c):
    """Publish the package to PyPI."""
    c.run("pip install twine")  # Ensure twine is installed
    c.run("twine upload dist/*")


@task(
    pre=[
        check_format,
        check_lint,
        check_type,
        test,
    ]
)
def ci(c):
    """Run all CI tasks (install, check_format, check_lint, type check, and test)."""
    pass


@task(pre=[format, lint, ci])
def prep_ci(c):
    """Run all CI tasks (install, check_format, check_lint, type check, and test)."""
    pass


@task(pre=[build, publish])
def release(c):
    """Release the package (build and publish)."""
    pass


@task
def tree(c):
    """Print the directory tree."""
    c.run("sudo apt-get install tree")
    c.run("tree -I '__pycache__' . > tree.txt")


@task
def bump_version(c):
    """Bump the version number in the version.py file."""

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
