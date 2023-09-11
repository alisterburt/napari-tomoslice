import napari
import numpy as np

from napari_tomoslice._constants import (
    TOMOGRAM_LAYER_NAME,
    PLANE_NORMAL_VECTOR,
    PLANE_THICKNESS,
)


def add_tomogram_to_viewer(
    tomogram: np.ndarray,
    viewer: napari.viewer.Viewer
):
    """Add a volume to the viewer in slicer mode, replacing if already present."""
    center = np.array(tomogram.shape) / 2
    kwargs = {
        'data': tomogram,
        'name': TOMOGRAM_LAYER_NAME,
        'colormap': 'gray_r',
        'rendering': 'minip',
        'blending': 'translucent',
        'depiction': 'plane',
        'plane': {
            'position': center,
            'normal': PLANE_NORMAL_VECTOR,
            'thickness': PLANE_THICKNESS,
        }
    }
    if TOMOGRAM_LAYER_NAME not in viewer.layers:
        viewer.add_image(**kwargs)
    else:
        layer = viewer.layers[TOMOGRAM_LAYER_NAME]
        for name, value in kwargs.items():
            setattr(layer, name, value)
    viewer.camera.angles = (0, 10, -20)
