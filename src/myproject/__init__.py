from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _package_version

from .core import greet

try:
    __version__ = _package_version("template-python")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__", "greet"]
