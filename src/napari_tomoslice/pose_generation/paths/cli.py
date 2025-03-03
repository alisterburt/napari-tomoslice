import typer

pose_generation_paths_cli = typer.Typer(
    name='paths',
    no_args_is_help=True,
    help='generate particle poses from path annotations')
