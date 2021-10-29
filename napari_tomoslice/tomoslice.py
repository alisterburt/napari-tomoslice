from typing import Optional
from functools import partial

import napari
import napari.layers
import mrcfile
import numpy as np

from .plane_controls import shift_plane_along_normal, set_plane_normal_axis


class TomoSlice:
    def __init__(self, viewer: napari.Viewer):
        self.viewer = viewer
        self.volume_layer: Optional[napari.layers.Image] = None
        self.plane_layer: Optional[napari.layers.Image] = None

        self.viewer.dims.ndisplay = 3

    def open_tomogram(self, tomogram_file: str):
        with mrcfile.open(tomogram_file) as mrc:
            tomogram = mrc.data
        self.add_volume_layer(tomogram)
        self.add_plane_layer(tomogram)
        self.connect_callbacks()
        self.viewer.reset_view()
        self.viewer.camera.angles = (140, -55, -140)
        self.viewer.camera.zoom = 0.8

    def close_tomogram(self):
        self.disconnect_callbacks()
        for layer in self.plane_layer, self.volume_layer:
            self.viewer.layers.remove(layer)

    def add_volume_layer(self, tomogram: np.ndarray):
        self.volume_layer = self.viewer.add_image(
            data=tomogram,
            name='tomogram',
            colormap='gray',
            rendering='minip'
        )

    def add_plane_layer(self, tomogram: np.ndarray):
        plane_parameters = {
            'enabled': True,
            'position': np.array(tomogram.shape) / 2,
            'normal': (1, 0, 0),
            'thickness': 5,
        }
        self.plane_layer = self.viewer.add_image(
            data=tomogram,
            name='plane',
            colormap='gray',
            rendering='minip',
            experimental_slicing_plane=plane_parameters
        )

    def connect_callbacks(self):
        self._mouse_drag_callback = partial(
            shift_plane_along_normal, layer=self.plane_layer
        )
        self.viewer.mouse_drag_callbacks.append(
            self._mouse_drag_callback
        )
        for key in 'xyz':
            callback = partial(
                set_plane_normal_axis, layer=self.plane_layer, axis=key
            )
            self.viewer.bind_key(key, callback)

    def disconnect_callbacks(self):
        self.viewer.mouse_drag_callbacks.remove(self._mouse_drag_callback)
        for key in 'xyz':
            self.viewer.keymap.pop(key.upper())


