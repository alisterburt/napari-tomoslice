import typer

from napari_tomoslice._constants import POSE_CONVERSION_CLI_NAME

pose_conversion_cli = typer.Typer(name=POSE_CONVERSION_CLI_NAME, no_args_is_help=True)