from pathlib import Path

import napari
import typer

cli = typer.Typer()


@cli.command()
def napari_tomoslice(tomogram_file: Path = typer.Argument(
    None,
    exists=True,
    file_okay=True,
    readable=True,
)):
    """An interactive tomogram slice viewer in napari.

    Controls:
    x/y/z - align normal vector along x/y/z axis
    click and drag plane - shift plane along its normal vector
    alt-click - add point on plane (if points layer is active)
    o - align plane normal to view direction
    [] - decrease/increase plane thickness
    """
    viewer = napari.Viewer()
    _, tomoslice_widget = viewer.window.add_plugin_dock_widget(
        plugin_name='napari-tomoslice'
    )
    if tomogram_file is not None:
        tomoslice_widget.tomoslice.open_tomogram(tomogram_file)
        tomoslice_widget.update_widget_visibility(tomogram_opened=True)
    napari.run()
