import typer

from .cli import pose_generation_cli as pose_generation_cli

pose_generation_paths_cli = typer.Typer(name='paths', no_args_is_help=True)


@pose_generation_paths_cli.command(name='backbone')
def generate_poses_filaments_backbone():
    print('bla')


@pose_generation_paths_cli.command(name='rings')
def generate_poses_filaments_rings():
    print('bla')


@pose_generation_paths_cli.command(name='helix')
def generate_poses_filaments_rings():
    print('bla')


pose_generation_cli.add_typer(pose_generation_paths_cli)
