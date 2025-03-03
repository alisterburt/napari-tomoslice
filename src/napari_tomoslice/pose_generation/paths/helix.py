from pathlib import Path

import numpy as np
import pandas as pd
import starfile
import typer
from morphosamplers import Path as MorphoPath, path_samplers
from scipy.spatial.transform import Rotation as R

from napari_tomoslice.console import console
from napari_tomoslice.pose_generation.cli import pose_generation_cli as pose_generation_cli
from .cli import pose_generation_paths_cli

@pose_generation_paths_cli.command(name='helix', no_args_is_help=True,
                                   help='evenly spaced particle poses along the annotated helical path')
def generate_poses_paths_helix(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
    distance_between_particles: float = typer.Option(...),
    twist: float = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_paths.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')

    # empty list to store per-path dataframes
    path_dfs = []

    # iterate over files and paths in each file
    for file in annotation_files:
        # read file, find paths and tilt series id
        df = starfile.read(file)
        grouped_paths = df.groupby('path_id')
        tilt_series_id = file.stem.rstrip('_paths')
        console.log(f'Found {grouped_paths.ngroups} paths in {file.name}')

        for path_id, path_data in grouped_paths:
            # construct morphosamplers Path for sampling
            control_points_xyz = path_data[['x', 'y', 'z']].to_numpy()
            try:
                path_df = _generate_pose_df_helix(
                    control_points_xyz=control_points_xyz,
                    spacing=distance_between_particles,
                    twist=twist,
                    path_id=path_id,
                    tilt_series_id=tilt_series_id
                )
                path_dfs.append(path_df)
                console.log(f'Generated {len(path_df)} particles for path {path_id} in {tilt_series_id}')
            except ValueError:
                console.log(f'Could not generate pose for path {path_id} in {tilt_series_id}')

    # write output to disk
    final_df = pd.concat(path_dfs)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}...')
    starfile.write({"particles": final_df}, output_star_file, overwrite=True)
    console.log('Done!', style="bold green")

def _generate_pose_df_helix(control_points_xyz: np.ndarray, spacing: float,
                            twist: float, path_id: int, tilt_series_id: str) -> pd.DataFrame:
    # create a morphosamplers Path object
    path = MorphoPath(control_points=control_points_xyz)

    # sample poses following a helical path along the backbone
    helical_pose_sampler = path_samplers.HelicalPoseSampler(
        spacing=spacing, twist=twist
    )
    poses = helical_pose_sampler.sample(path)
    # Extract positions and euler angles
    positions = poses.positions
    euler_angles = (
        R.from_matrix(poses.orientations)
        .inv()
        .as_euler(seq='ZYZ', degrees=True)
    )

    # construct dataframe
    particle_pose_data = {
        'x': positions[:, 0],
        'y': positions[:, 1],
        'z': positions[:, 2],
        'rot': euler_angles[:, 0],
        'tilt': euler_angles[:, 1],
        'psi': euler_angles[:, 2],
        'manifold_id': [f"{path_id}"] * len(positions),
        'tilt_series_id': [tilt_series_id] * len(positions)
    }
    return pd.DataFrame(particle_pose_data)


pose_generation_cli.add_typer(pose_generation_paths_cli)
