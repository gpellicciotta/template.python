"""Expose the package version and public greeting API."""

from support_python import get_package_version

from .core import greet

#: Installed distribution version, or a fallback when package metadata is unavailable.
__version__ = get_package_version("template-python")

__all__ = ["__version__", "greet"]
