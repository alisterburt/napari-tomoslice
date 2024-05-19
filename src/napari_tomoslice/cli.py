import warnings
from datetime import datetime
from pathlib import Path

import typer

from napari_tomoslice._cli import cli
from napari_tomoslice.console import console
from napari_tomoslice.tomoslice import TomoSliceApplication, AnnotationMode

datetime_string = f'{datetime.now()}'.replace(' ', '_').replace('-', '_')

@cli.command(no_args_is_help=True)
def napari_tomoslice(
    tomogram_directory: Path | None = None,
    file_pattern: str = typer.Option('*.mrc'),
    annotation_directory: Path = typer.Option(Path(f'tomoslice_{datetime_string}')),
    mode: AnnotationMode = typer.Option(..., show_default=False),
):
    console.log('starting napari-tomoslice')

    console.log('launching napari viewer')
    import napari
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
