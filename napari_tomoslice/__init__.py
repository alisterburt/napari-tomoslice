
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._qt.tomoslice import napari_experimental_provide_dock_widget

