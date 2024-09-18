import typer

from napari_tomoslice._constants import POSE_EXPORT_CLI_NAME

pose_export_cli = typer.Typer(
    name=POSE_EXPORT_CLI_NAME,
    no_args_is_help=True,
    help="export compatible metadata for a variety of different software packages",
)