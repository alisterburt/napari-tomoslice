from pathlib import Path

import starfile
import typer
import pandas as pd

from .cli import pose_generation_cli
from napari_tomoslice.console import console


@pose_generation_cli.command(name='points', no_args_is_help=True,
                             help='generate particle poses from point annotations')
def generate_poses_points(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_points.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    dfs = []
    for file in annotation_files:
        tilt_series_id = file.stem.rstrip('_points')
        df = starfile.read(file)
        console.log(f'Found {len(df)} particles in {file.name}')
        df['tilt_series_id'] = [tilt_series_id] * len(df)
        dfs.append(df)

    df = pd.concat(dfs)
    sorted_df = df.sort_values('tilt_series_id')
    starfile.write(sorted_df, output_star_file)
    console.log(f'Writing {len(df)} particles into {output_star_file}')
    console.log('Done!', style="bold green")
