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
        install_dependencies,
        install_dev_dependencies,
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
