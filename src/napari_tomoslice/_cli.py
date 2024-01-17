import typer

from napari_tomoslice._constants import CLI_NAME

cli = typer.Typer(name=CLI_NAME, no_args_is_help=True, add_completion=False)
