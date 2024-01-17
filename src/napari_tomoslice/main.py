import warnings
from pathlib import Path

from napari_tomoslice._cli import cli
from napari_tomoslice.console import console
from napari_tomoslice.tomoslice import TomoSliceApplication, AnnotationMode


@cli.command(no_args_is_help=True)
def napari_tomoslice(
    tomogram_file: Path | None = None,
    tomogram_directory: Path | None = None,
    tomogram_glob_pattern: str = '*.mrc',
    annotation_directory: Path | None = None,
    annotation_mode: AnnotationMode = AnnotationMode.DISABLED
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
        tomogram_file=tomogram_file,
        tomogram_directory=tomogram_directory,
        tomogram_glob_pattern=tomogram_glob_pattern,
    )
    napari.run()
