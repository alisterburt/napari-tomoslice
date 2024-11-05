import os
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import TypeVar, Optional

import napari
import napari_threedee as n3d
import starfile
from napari_threedee.annotators.constants import N3D_METADATA_KEY, ANNOTATION_TYPE_KEY

from napari_tomoslice._constants import (
    TOMOGRAM_BROWSER_WIDGET_NAME,
    TOMOGRAM_LAYER_NAME,
    PLANE_CONTROLS_HELP_TEXT,
    DISABLED_ANNOTATOR_HELP_TEXT,
    POINT_ANNOTATOR_HELP_TEXT,
    PATH_ANNOTATOR_HELP_TEXT,
    SPHERE_ANNOTATOR_HELP_TEXT, POINT_ANNOTATION_FACE_COLOR,
    DIPOLE_ANNOTATOR_HELP_TEXT,
)
from napari_tomoslice.console import console
from napari_tomoslice.io import read_volume, save_points, save_paths, save_spheres, save_dipoles
from napari_tomoslice.io.dipoles import load_dipoles
from napari_tomoslice.io.paths import load_paths
from napari_tomoslice.io.points import load_points
from napari_tomoslice.io.spheres import load_spheres
from napari_tomoslice.utils import add_tomogram_to_viewer, get_annotation_layer
from napari_tomoslice.widgets import TomoSliceWidget

Annotator = TypeVar('Annotator')


class AnnotationMode(Enum):
    POINTS = 'points'
    PATHS = 'paths'
    SPHERES = 'spheres'
    DIPOLES = 'dipoles'


class TomoSliceApplication:
    viewer: napari.viewer.Viewer
    annotator: Optional[Annotator]

    annotation_directory: Optional[Path]
    annotation_mode: AnnotationMode

    tomogram_file: Optional[Path]
    tomogram_directory: Optional[Path]

    def __init__(
        self,
        viewer: napari.viewer.Viewer,
        tomogram_file: Optional[Path] = None,
        tomogram_directory: Optional[Path] = None,
        tomogram_glob_pattern: str = '*.mrc',
        annotation_mode: AnnotationMode = AnnotationMode.POINTS,
        annotation_directory: Optional[Path] = None,
    ):
        self.viewer = viewer
        self.annotator = None
        self._annotation_directory = annotation_directory
        self._annotation_mode = annotation_mode
        self._tomogram_file = tomogram_file
        self._tomogram_directory = tomogram_directory

        if tomogram_file is not None and tomogram_directory is None:
            self._tomogram_directory = tomogram_file.absolute().parent

        # instantiate widgets
        self.widget = TomoSliceWidget(
            slicer=self,
            annotation_mode=self.annotation_mode,
            directory=self.tomogram_directory,
            glob_pattern=tomogram_glob_pattern
        )

        # add widgets to viewer
        self.viewer.window.add_dock_widget(
            self.widget,
            name=TOMOGRAM_BROWSER_WIDGET_NAME,
            area='right',
            allowed_areas=['right'],
        )

        # keybindings
        self.save_annotations = self.viewer.bind_key('s')(self.save_annotation)

        # callbacks
        self.widget.save_button.clicked.connect(self.save_annotation)

        # help-text display
        self.viewer.text_overlay.visible = True
        self.viewer.text_overlay.position = 'top_left'
        self.viewer.text_overlay.text = \
            f"{DISABLED_ANNOTATOR_HELP_TEXT}"

        # force viewer updates
        if tomogram_file is not None:
            self.load_tomogram(tomogram_file)

        self.annotation_directory = self._annotation_directory

    @property
    def annotation_mode(self) -> str:
        return self._annotation_mode.value

    @property
    def annotation_directory(self) -> Path:
        return self._annotation_directory

    @annotation_directory.setter
    def annotation_directory(self, value: PathLike):
        self._annotation_directory = Path(value) if value is not None else None

    @property
    def tomogram_directory(self) -> Path:
        return self._tomogram_directory

    @property
    def tomogram_file(self) -> Path:
        return self._tomogram_file

    @tomogram_file.setter
    def tomogram_file(self, value: os.PathLike):
        self._tomogram_file = Path(value)

    @property
    def annotation_file(self) -> Path:
        return self.annotation_directory / f'{self.tomogram_file.stem}_{self.annotation_mode}.star'

    def load_tomogram(self, path: Path):
        console.log(f'loading tomogram from {path}')
        volume = read_volume(path)
        console.log(f'array of shape {volume.shape} loaded')
        add_tomogram_to_viewer(tomogram=volume, viewer=self.viewer, show_bounding_box=True)
        console.log('tomogram added to viewer')

        self.remove_non_tomogram_layers()
        self.tomogram_file = path
        self.start_annotation()

    def start_annotation(self):
        if self.annotation_file.exists():
            self.load_annotation(self.annotation_file)
        elif self.annotation_mode == 'points':
            self.new_point_annotation()
        elif self.annotation_mode == 'paths':
            self.new_path_annotation()
        elif self.annotation_mode == 'spheres':
            self.new_sphere_annotation()
        elif self.annotation_mode == 'dipoles':
            self.new_dipole_annotation()
        self.select_tomogram_layer()

    def select_tomogram_layer(self):
        self.viewer.layers.selection = [self.viewer.layers[TOMOGRAM_LAYER_NAME]]

    def remove_non_tomogram_layers(self):
        # add outer loop to workaround bug which prevents removal
        # probable cause: layer indices aren't updated properly in napari when layers are removed
        # this is fine...
        for i in range(10):
            for layer in self.viewer.layers:
                if layer.name != TOMOGRAM_LAYER_NAME:
                    self.viewer.layers.remove(layer)

    def load_annotation(self, path: Path, *args, **kwargs):
        # get annotation type
        data = starfile.read(path, always_dict=True)
        annotation_type = list(data.keys())[0]

        # test
        if annotation_type == 'points':
            layer = load_points(path)
            self.activate_point_annotator(layer)
        elif annotation_type == 'paths':
            layer = load_paths(path)
            self.activate_path_annotator(layer)
        elif annotation_type == 'spheres':
            layer = load_spheres(path)
            self.activate_sphere_annotator(layer)
        elif annotation_type == 'dipoles':
            layer = load_dipoles(path)
            self.activate_dipole_annotator(layer)
        else:
            raise RuntimeError('unsupported annotation type')
        self.select_tomogram_layer()

    def save_annotation(self, *args, **kwargs):
        layer = get_annotation_layer(viewer=self.viewer, annotation_mode=self.annotation_mode)
        annotation_type = layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY]
        self.annotation_directory.mkdir(exist_ok=True, parents=True)
        if annotation_type == 'points':
            save_points(layer=layer, path=self.annotation_file)
        elif annotation_type == 'path':
            save_paths(layer=layer, path=self.annotation_file)
        elif annotation_type == 'spheres':
            save_spheres(layer=layer, path=self.annotation_file)
        elif annotation_type == 'dipoles':
            save_dipoles(layer=layer, path=self.annotation_file)
        else:
            raise RuntimeError('unsupported annotation type')
        console.log(f'{annotation_type} annotation saved for {self.tomogram_file} in {self.annotation_directory}')

    def new_point_annotation(self):
        layer = n3d.data_models.N3dPoints(data=[]).as_layer()
        layer.current_face_color = POINT_ANNOTATION_FACE_COLOR
        self.activate_point_annotator(layer)

    def activate_point_annotator(self, points_layer):
        self.viewer.add_layer(points_layer)
        self.annotator = n3d.annotators.PointAnnotator(
            viewer=self.viewer,
            image_layer=self.viewer.layers[TOMOGRAM_LAYER_NAME],
            points_layer=points_layer,
            enabled=True
        )
        console.log('point annotator started')
        self.viewer.layers.selection.active = self.viewer.layers[TOMOGRAM_LAYER_NAME]
        self.viewer.text_overlay.text = \
            f"{PLANE_CONTROLS_HELP_TEXT}\n{POINT_ANNOTATOR_HELP_TEXT}"

    def new_path_annotation(self):
        points_layer = n3d.data_models.N3dPaths(data=[]).as_layer()
        self.activate_path_annotator(points_layer)

    def activate_path_annotator(self, points_layer):
        self.viewer.add_layer(points_layer)
        self.annotator = n3d.annotators.PathAnnotator(
            viewer=self.viewer,
            image_layer=self.viewer.layers[TOMOGRAM_LAYER_NAME],
            points_layer=points_layer,
            enabled=True,
        )
        console.log('path annotator started')
        self.viewer.text_overlay.text = \
            f"{PLANE_CONTROLS_HELP_TEXT}\n{PATH_ANNOTATOR_HELP_TEXT}"

    def new_sphere_annotation(self):
        points_layer = n3d.data_models.N3dSpheres(centers=[], radii=[]).as_layer()
        self.activate_sphere_annotator(points_layer)

    def activate_sphere_annotator(self, points_layer):
        self.viewer.add_layer(points_layer)
        self.annotator = n3d.annotators.SphereAnnotator(
            viewer=self.viewer,
            image_layer=self.viewer.layers[TOMOGRAM_LAYER_NAME],
            points_layer=points_layer,
            enabled=True,
        )
        console.log('sphere annotator started')
        self.viewer.text_overlay.text = \
            f"{PLANE_CONTROLS_HELP_TEXT}\n{SPHERE_ANNOTATOR_HELP_TEXT}"

    def new_dipole_annotation(self):
        points_layer = n3d.data_models.N3dDipoles(data=[]).as_layer()
        self.activate_dipole_annotator(points_layer)

    def activate_dipole_annotator(self, points_layer):
        self.viewer.add_layer(points_layer)
        self.annotator = n3d.annotators.DipoleAnnotator(
            viewer=self.viewer,
            image_layer=self.viewer.layers[TOMOGRAM_LAYER_NAME],
            points_layer=points_layer,
            enabled=True,
        )
        console.log('dipole annotator started')
        self.viewer.text_overlay.text = \
            f"{PLANE_CONTROLS_HELP_TEXT}\n{DIPOLE_ANNOTATOR_HELP_TEXT}"
