import napari
import numpy as np
from napari_threedee.annotators.constants import N3D_METADATA_KEY, ANNOTATION_TYPE_KEY

from napari_tomoslice._constants import (
    TOMOGRAM_LAYER_NAME,
    PLANE_NORMAL_VECTOR,
    PLANE_THICKNESS,
)


def add_tomogram_to_viewer(
    tomogram: np.ndarray,
    viewer: napari.viewer.Viewer,
    show_bounding_box: bool,
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
        layer = viewer.add_image(**kwargs)
    else:
        layer = viewer.layers[TOMOGRAM_LAYER_NAME]
        for name, value in kwargs.items():
            setattr(layer, name, value)
        layer.reset_contrast_limits_range()
        layer.reset_contrast_limits()
    layer.bounding_box.visible = show_bounding_box
    viewer.reset_view()
    viewer.camera.center = center
    viewer.camera.zoom *= 0.5
    viewer.camera.angles = (-8, 23, -18)


def get_annotation_layer(viewer: napari.viewer.Viewer, annotation_mode=None):
    selected_layer = viewer.layers.selection.active

    # handle multiple active layers
    if type(selected_layer) == list and annotation_mode is None:
        raise RuntimeError(
            'Ambiguous: please select the layer containing the annotation you want to save.'
        )

    #
    if N3D_METADATA_KEY not in selected_layer.metadata:
        annotation_layers = [
            layer
            for layer in viewer.layers
            if N3D_METADATA_KEY in layer.metadata
        ]
        if len(annotation_layers) == 1:
            annotation_layer = annotation_layers[0]
        elif len(annotation_layers) > 1 and annotation_mode is not None:
            layer_to_annotation_type = {
                layer: layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY]
                for layer
                in annotation_layers
                if layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY] == annotation_mode
            }
            if len(layer_to_annotation_type) == 1:
                annotation_layer = list(layer_to_annotation_type.keys())[0]
        else:
            raise RuntimeError(
                'Ambiguous: please select the layer containing the annotation you want to save.'
            )
    else:
        annotation_layer = selected_layer
    return annotation_layer
