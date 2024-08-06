import warnings

from pathlib import Path

from datetime import datetime

import typer

from napari_tomoslice._constants import ANNOTATION_CLI_NAME
from napari_tomoslice.annotation.tomoslice_app import AnnotationMode, TomoSliceApplication
from napari_tomoslice.console import console


current_time = datetime.now()
datetime_string = current_time.strftime("%Y_%m_%d_%H:%M:%S")

def annotation_cli(
    tomogram_directory: Path = None,
    file_pattern: str = typer.Option('*.mrc'),
    annotation_directory: Path = typer.Option(default=datetime_string),
    mode: AnnotationMode = typer.Option(..., show_default=False),
):
    console.log('starting napari-tomoslice')

    console.log('launching napari viewer')
    import napari  # do napari import locally to avoid before launching cli
    viewer = napari.Viewer(
        title='napari-tomoslice',
        ndisplay=3,
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        viewer.window.qt_viewer.set_welcome_visible(False)
    console.log('viewer launched')

    app = TomoSliceApplication(
        viewer=viewer,
        tomogram_directory=tomogram_directory,
        tomogram_glob_pattern=file_pattern,
        annotation_directory=annotation_directory,
        annotation_mode=mode,
    )
    napari.run()