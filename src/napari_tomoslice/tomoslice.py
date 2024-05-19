import os
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import TypeVar, Optional

import napari
import napari_threedee as n3d
import starfile
from napari_threedee.annotators.constants import N3D_METADATA_KEY, ANNOTATION_TYPE_KEY

from napari_tomoslice.io import read_volume, save_points, save_paths, save_spheres
from napari_tomoslice.io.paths import load_paths
from napari_tomoslice.io.points import load_points
from napari_tomoslice.io.spheres import load_spheres
from napari_tomoslice.utils import add_tomogram_to_viewer, get_annotation_layer
from napari_tomoslice.widgets import AnnotatorControls, DirectoryBrowser
from napari_tomoslice.console import console
from napari_tomoslice._constants import (
    CONTROLS_WIDGET_NAME,
    TOMOGRAM_BROWSER_WIDGET_NAME,
    TOMOGRAM_LAYER_NAME,
    PLANE_CONTROLS_HELP_TEXT,
    DISABLED_ANNOTATOR_HELP_TEXT,
    POINT_ANNOTATOR_HELP_TEXT,
    PATH_ANNOTATOR_HELP_TEXT,
    SPHERE_ANNOTATOR_HELP_TEXT,
)

Annotator = TypeVar('Annotator')


class AnnotationMode(Enum):
    POINT = 'point'
    PATH = 'path'
    SPHERE = 'sphere'


class TomoSliceApplication:
    viewer: napari.viewer.Viewer
    annotator_controls: AnnotatorControls
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
        annotation_mode: AnnotationMode = AnnotationMode.POINT,
        annotation_directory: Optional[Path] = None,
    ):
        self.viewer = viewer
        self.annotator = None
        self._annotation_directory = annotation_directory
        self._annotation_mode = annotation_mode
        self._tomogram_file = tomogram_file

        if tomogram_file is not None and tomogram_directory is None:
            tomogram_directory = tomogram_file.absolute().parent

        # instantiate widgets
        self.annotator_controls = AnnotatorControls(
            application=self,
            annotation_directory=annotation_directory
        )
        self.tomogram_browser_widget = DirectoryBrowser(
            slicer=self,
            directory=tomogram_directory,
            glob_pattern=tomogram_glob_pattern
        )

        # add widgets to viewer
        self.viewer.window.add_dock_widget(
            self.annotator_controls,
            name=CONTROLS_WIDGET_NAME,
            area='left',
            allowed_areas=['left'],
        )
        self.viewer.window.add_dock_widget(
            self.tomogram_browser_widget,
            name=TOMOGRAM_BROWSER_WIDGET_NAME,
            area='right',
            allowed_areas=['right'],
        )

        # keybindings
        self.save_annotations = self.viewer.bind_key('s')(self.save_annotation)

        # callbacks
        annotator_buttons = self.annotator_controls.annotator_button_group
        annotator_buttons.point_button.clicked.connect(self.new_point_annotation)
        annotator_buttons.path_button.clicked.connect(self.new_path_annotation)
        annotator_buttons.sphere_button.clicked.connect(self.new_sphere_annotation)

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
    def annotation_mode(self) -> str | None:
        if self.annotator is None:
            return None
        else:
            return self.annotator.points_layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY]

    @property
    def annotation_directory(self) -> Path | None:
        return self._annotation_directory

    @annotation_directory.setter
    def annotation_directory(self, value: PathLike):
        self._annotation_directory = Path(value) if value is not None else None
        if value is not None:
            self.annotator_controls.annotation_directory_selector.line_edit.setText(
                str(self._annotation_directory)
            )
            self.annotator_controls.update_file_list()

    @property
    def tomogram_directory(self) -> Path | None:
        return self.tomogram_browser_widget.directory

    @tomogram_directory.setter
    def tomogram_directory(self, value: str | Path):
        self.tomogram_browser_widget.directory = value

    @property
    def tomogram_file(self) -> Path | None:
        return self._tomogram_file

    @tomogram_file.setter
    def tomogram_file(self, value: os.PathLike):
        self._tomogram_file = Path(value)
        self.annotator_controls.update_file_list()

    def load_tomogram(self, path: Path):
        console.log(f'loading tomogram from {path}')
        volume = read_volume(path)
        console.log(f'array of shape {volume.shape} loaded')
        add_tomogram_to_viewer(tomogram=volume, viewer=self.viewer)
        console.log('tomogram added to viewer')
        self.tomogram_file = path

    def load_annotation(self, path: Path, *args, **kwargs):
        # get annotation type
        data = starfile.read(path, always_dict=True)
        annotation_type = list(data.keys())[0]

        # test
        if annotation_type == 'points':
            layer = load_points(path)
            self.activate_point_annotator(layer)
        elif annotation_type == 'path':
            layer = load_paths(path)
            self.activate_path_annotator(layer)
        elif annotation_type == 'spheres':
            layer = load_spheres(path)
            self.activate_sphere_annotator(layer)
        else:
            raise RuntimeError('unsupported annotation type')

    def save_annotation(self, *args, **kwargs):
        layer = get_annotation_layer(viewer=self.viewer, annotation_mode=self.annotation_mode)
        annotation_type = layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY]
        self.annotation_directory.mkdir(exist_ok=True, parents=True)
        output_file = self.annotation_directory / f'{self.tomogram_file.stem}_{annotation_type}.star'
        if annotation_type == 'points':
            save_points(layer=layer, path=output_file)
        elif annotation_type == 'path':
            save_paths(layer=layer, path=output_file)
        elif annotation_type == 'spheres':
            save_spheres(layer=layer, path=output_file)
        else:
            raise RuntimeError('unsupported annotation type')
        self.annotator_controls.update_file_list()

    def new_point_annotation(self):
        points_layer = n3d.data_models.N3dPoints(data=[]).as_layer()
        self.activate_point_annotator(points_layer)

    def activate_point_annotator(self, points_layer):
        points_layer.face_color = 'cornflowerblue'
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
