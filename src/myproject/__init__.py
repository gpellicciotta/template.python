"""Expose the package version and public greeting API."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _package_version

from .core import greet

#: Installed distribution version, or a fallback when package metadata is unavailable.
try:
    __version__ = _package_version("template-python")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__", "greet"]
