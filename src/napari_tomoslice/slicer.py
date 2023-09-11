from enum import Enum, auto
from os import PathLike
from pathlib import Path
from typing import TypeVar, Optional

import napari
import napari_threedee as n3d
from napari_threedee.annotators.constants import N3D_METADATA_KEY, ANNOTATION_TYPE_KEY

from napari_tomoslice.io import read_volume, save_points, save_paths, save_spheres
from napari_tomoslice.utils import add_tomogram_to_viewer
from napari_tomoslice.widgets import SlicerControls, FolderBrowser
from napari_tomoslice.console import console
from napari_tomoslice._constants import (
    CONTROLS_WIDGET_NAME,
    FOLDER_BROWSER_WIDGET_NAME,
    TOMOGRAM_LAYER_NAME,
    PLANE_CONTROLS_HELP_TEXT,
    DISABLED_ANNOTATOR_HELP_TEXT,
    POINT_ANNOTATOR_HELP_TEXT,
    PATH_ANNOTATOR_HELP_TEXT,
    SPHERE_ANNOTATOR_HELP_TEXT,
)

Annotator = TypeVar('Annotator')


class AnnotationMode(Enum):
    DISABLED = auto()
    POINT = auto()
    PATH = auto()
    SPHERE = auto()


class Slicer:
    viewer: napari.viewer.Viewer
    controls_widget: SlicerControls
    annotator: Optional[Annotator]

    tomogram_file: Optional[Path]
    output_folder: Optional[Path]
    annotation_mode: AnnotationMode

    def __init__(
        self,
        viewer: napari.viewer.Viewer,
        mode: AnnotationMode = AnnotationMode.DISABLED,
        tomogram_file: Optional[Path] = None,
        output_folder: Optional[Path] = None,
        glob_pattern: str = '*'
    ):
        self.viewer = viewer
        self._tomogram_file = tomogram_file
        self._output_folder = output_folder
        self.annotator = None
        self._annotation_mode = mode

        self.controls_widget = SlicerControls(slicer=self)
        self.folder_browser_widget = FolderBrowser(
            slicer=self, directory=output_folder, glob_pattern=glob_pattern
        )

        self.viewer.window.add_dock_widget(
            self.controls_widget,
            name=CONTROLS_WIDGET_NAME,
            area='left',
            allowed_areas=['left'],
        )
        self.viewer.window.add_dock_widget(
            self.folder_browser_widget,
            name=FOLDER_BROWSER_WIDGET_NAME,
            area='right',
            allowed_areas=['right'],
        )

        self.save_annotations = self.viewer.bind_key('s')(self.save_annotation)
        self.viewer.text_overlay.visible = True
        self.viewer.text_overlay.position = 'top_left'
        self.viewer.text_overlay.text = \
            f"{DISABLED_ANNOTATOR_HELP_TEXT}"

        self.annotation_mode = self._annotation_mode



    @property
    def tomogram_file(self) -> Path | None:
        return self._tomogram_file

    @tomogram_file.setter
    def tomogram_file(self, value: PathLike):
        self._tomogram_file = Path(value) if value is not None else None

        # update gui

        self.load_tomogram(self._tomogram_file)

    @property
    def output_folder(self) -> Path | None:
        return self._output_folder

    @output_folder.setter
    def output_folder(self, value: PathLike):
        self._output_folder = Path(value) if value is not None else None
        if value is not None:
            self.folder_browser_widget.directory = Path(value)

        # update gui
        self.controls_widget.tomogram_selector.line_edit.setText(
            str(self._tomogram_file)
        )

    @property
    def annotation_mode(self) -> AnnotationMode:
        return self._annotation_mode

    @annotation_mode.setter
    def annotation_mode(self, value: AnnotationMode):
        self._annotation_mode = value

        # ensure correct annotator is loaded
        if TOMOGRAM_LAYER_NAME not in self.viewer.layers:
            if self._annotation_mode != AnnotationMode.DISABLED:
                console.log('annotation mode changed but no tomogram in viewer')
        else:
            console.log(f'{self._annotation_mode.value} selected')
            self.start_annotator()

        # update gui
        buttons = self.controls_widget.annotator_button_group
        mode_to_button = {
            AnnotationMode.DISABLED: 999,
            AnnotationMode.POINT: buttons.point_button,
            AnnotationMode.PATH: buttons.path_button,
            AnnotationMode.SPHERE: buttons.sphere_button,
        }
        for button in buttons:
            if button is not mode_to_button[value]:
                button.setChecked(False)

    def load_tomogram(self, path: Path):
        console.log(f'loading tomogram from {path}')
        volume = read_volume(path)
        console.log(f'array of shape {volume.shape} loaded')
        add_tomogram_to_viewer(tomogram=volume, viewer=self.viewer)
        console.log('tomogram added to viewer')

    def save_annotation(self, *args, **kwargs):
        layer = _get_annotation_layer(viewer=self.viewer)
        annotation_type = layer.metadata[N3D_METADATA_KEY][ANNOTATION_TYPE_KEY]
        self.output_folder.mkdir(exist_ok=True, parents=True)
        output_file = self.output_folder / f'{self.tomogram_file.stem}_{annotation_type}.star'
        if annotation_type == 'points':
            save_points(layer=layer, path=output_file)
        elif annotation_type == 'paths':
            save_paths(layer=layer, path=output_file)
        elif annotation_type == 'spheres':
            save_spheres(layer=layer, path=output_file)
        else:
            raise RuntimeError('unsupported annotation type')

    def start_annotator(self):
        if self.annotator is not None:  # disable active annotator
            self.annotator.enabled = False

        if self.annotation_mode is AnnotationMode.POINT:
            self.start_point_annotator()
        elif self.annotation_mode is AnnotationMode.PATH:
            self.start_path_annotator()
        elif self.annotation_mode is AnnotationMode.SPHERE:
            self.start_sphere_annotator()

    def start_point_annotator(self):
        points_layer = n3d.data_models.N3dPoints(data=[]).as_layer()
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

    def start_path_annotator(self):
        points_layer = n3d.data_models.N3dPaths(data=[]).as_layer()
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

    def start_sphere_annotator(self):
        points_layer = n3d.data_models.N3dSpheres(centers=[], radii=[]).as_layer()
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


def _get_annotation_layer(viewer: napari.viewer.Viewer):
    selected_layer = viewer.layers.selection.active
    if type(selected_layer) == list:
        raise RuntimeError(
            'One layer must be selected, \
            select the layer containing the annotation you want to save.'
        )
    if N3D_METADATA_KEY not in selected_layer.metadata:
        annotation_layers = [
            layer
            for layer in viewer.layers
            if N3D_METADATA_KEY in layer.metadata
        ]
        if len(annotation_layers) == 1:
            annotation_layer = annotation_layers[0]
        else:
            raise RuntimeError(
                'Please select the layer containing the annotation you want to save.'
            )
    else:
        annotation_layer = selected_layer
    return annotation_layer

