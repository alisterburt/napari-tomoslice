from pathlib import Path

import typer

from .cli import pose_generation_cli

@pose_generation_cli.command(name='points', no_args_is_help=True)
def generate_poses_points(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
):
    print('lala')