from pathlib import Path

from napari_tomoslice._cli import cli
from napari_tomoslice.console import console
from napari_tomoslice.slicer import Slicer


@cli.command()
def napari_tomoslice(
    tomogram_file: Path | None = None
):
    console.log('starting napari-tomoslice')

    console.log('launching napari viewer')
    import napari
    viewer = napari.Viewer(
        title='napari-tomoslice',
        ndisplay=3,
    )
    viewer.window.qt_viewer.set_welcome_visible(False)
    console.log('viewer launched')

    slicer = Slicer(viewer=viewer)
    if tomogram_file is not None:
        slicer.load_tomogram(tomogram_file)

    napari.run()
