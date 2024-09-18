import typer

from .._constants import POSE_GENERATION_CLI_NAME

pose_generation_cli = typer.Typer(
    name=POSE_GENERATION_CLI_NAME,
    no_args_is_help=True,
    help="generate particle poses from geometrical annotations",
)

