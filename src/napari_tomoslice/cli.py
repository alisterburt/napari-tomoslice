import typer

from napari_tomoslice._constants import TOMOSLICE_CLI_NAME, ANNOTATION_CLI_NAME
from napari_tomoslice.annotation import annotation_cli
from napari_tomoslice.pose_generation import pose_generation_cli
from napari_tomoslice.pose_conversion import pose_conversion_cli

cli = typer.Typer(name=TOMOSLICE_CLI_NAME, no_args_is_help=True, add_completion=False)

cli.command(no_args_is_help=True, name=ANNOTATION_CLI_NAME)(annotation_cli)
cli.add_typer(pose_generation_cli)
cli.add_typer(pose_conversion_cli)
