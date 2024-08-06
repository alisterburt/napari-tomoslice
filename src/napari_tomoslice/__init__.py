"""Tomogram visualisation and annotation in napari."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("napari-tomoslice")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Alister Burt"
__email__ = "alisterburt@gmail.com"

from .cli import cli