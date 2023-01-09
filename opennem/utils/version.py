import logging
from datetime import datetime
from enum import Enum
from pathlib import Path

try:
    import tomlkit
except ModuleNotFoundError:
    print("Could not import external package. virtualenv likely not activated.")

from packaging.version import parse

logger = logging.getLogger(__name__)


# get metadata from pyproject.toml
def get_project_meta() -> dict | None:
    pyproject = Path(__file__).parent / "../../pyproject.toml"

    if not pyproject.is_file():
        return None

    with pyproject.open() as pp_file:
        file_contents = pp_file.read()

    project_meta = None

    try:
        project_meta = tomlkit.parse(file_contents)
    except Exception as e:
        logger.error(f"Error parsing project metadata: {e}")
        return None

    return dict(project_meta)


# get version from VERSION file
def get_pkg_version() -> str | None:
    import pkgutil

    pkg_data = None

    try:
        pkg_data = pkgutil.get_data(__package__, "VERSION")
    except Exception:
        pass

    if not pkg_data:
        return None

    version = pkg_data.decode("utf-8").strip()

    del pkgutil

    return version


def get_scm_version() -> None:
    import os.path as pth

    try:
        from setuptools_scm import get_version

        get_version(root=pth.join("..", ".."), relative_to=__file__)
    except Exception:
        raise ImportError("setuptools_scm broken or not installed")


pkg_meta = get_project_meta()
version = None

if pkg_meta:
    CUR_YEAR = datetime.now().year
    poetry_meta = pkg_meta["tool"]["poetry"]
    project = str(poetry_meta["name"])
    copyright = f"{CUR_YEAR}, OpenNEM"
    version = str(poetry_meta["version"])
else:
    raise Exception("Could not read project meta. Likely virtualenv not activated")

release = version


class VersionPart(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


def get_version(version_part: VersionPart | None = None) -> str:
    if not version:
        return ""

    version_parsed = parse(version)

    if not version_part:
        return version

    if version_part == VersionPart.MAJOR:
        return str(version_parsed.major)

    if version_part == VersionPart.MINOR:
        return str(version_parsed.minor)

    if version_part == VersionPart.PATCH:
        return str(version_parsed.minor)

    return version
