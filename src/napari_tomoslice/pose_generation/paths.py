from pathlib import Path

import pandas as pd
import starfile
import typer
from morphosamplers import Path as MorphoPath, path_samplers
from scipy.spatial.transform import Rotation as R

from napari_tomoslice.console import console
from .cli import pose_generation_cli as pose_generation_cli

pose_generation_paths_cli = typer.Typer(name='paths', no_args_is_help=True)


@pose_generation_paths_cli.command(name='backbone', no_args_is_help=True)
def generate_poses_paths_backbone(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
    distance_between_particles: float = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_paths.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    if len(annotation_files) == 0:
        return

    # empty list to store per-path dataframes
    path_dfs = []

    # iterate over files and generate particle poses
    for file in annotation_files:
        # read file
        df = starfile.read(file)

        # isolate paths and determine tilt series identifier
        grouped_paths = df.groupby('path_id')
        tilt_series_id = file.stem.rstrip('_paths')
        console.log(f'Found {grouped_paths.ngroups} paths in {file.name}')

        for path_id, path_df in grouped_paths:
            # create a morphosamplers Path object
            control_points_xyz = path_df[['x', 'y', 'z']].values
            path = MorphoPath(control_points=control_points_xyz)

            # sample positions and orientations along the path
            pose_sampler = path_samplers.PoseSampler(spacing=distance_between_particles)
            poses = pose_sampler.sample(path)

            # Extract positions and euler angles
            positions = poses.positions
            euler_angles = (
                R.from_matrix(poses.orientations)
                .inv()
                .as_euler(seq='ZYZ', degrees=True)
            )

            # prepare dataframe for output
            particle_pose_data = {
                'x': poses.positions[:, -3],
                'y': positions[:, -2],
                'z': positions[:, -1],
                'rot': euler_angles[:, 0],
                'tilt': euler_angles[:, 1],
                'psi': euler_angles[:, 2],
                'path_id': [f"{path_id}"] * len(positions),
                'tilt_series_id': [tilt_series_id] * len(positions)
            }
            path_df = pd.DataFrame(particle_pose_data)
            path_dfs.append(path_df)
            console.log(f'Generated {len(path_df)} particles for path {path_id} in {tilt_series_id}')

    # write output file to disk
    df_out = pd.concat(path_dfs)
    console.log(f'Writing {len(df_out)} particles into {output_star_file}...')
    starfile.write({"paths": df_out}, output_star_file, overwrite=True)
    console.log('Done!')


@pose_generation_paths_cli.command(name='rings', no_args_is_help=True)
def generate_poses_paths_rings():
    print('coming soon...')


@pose_generation_paths_cli.command(name='helix', no_args_is_help=True)
def generate_poses_paths_helix(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
    distance_between_particles: float = typer.Option(...),
    twist: float = typer.Option(...),
):
    annotations_files = list(annotations_directory.glob('*_paths.star'))
    console.log(f'Found {len(annotations_files)} files in {annotations_directory}')
    all_dfs = []
    for file in annotations_files:
        tilt_series_id = file.stem.rstrip('_paths')
        df = starfile.read(file)
        num_paths = df['path_id'].nunique()
        console.log(f'Found {num_paths} paths in {file.name}')
        grouped_paths = df.groupby('path_id')
        for path_id, path_data in grouped_paths:
            control_points = path_data[['x', 'y', 'z']].values
            path = MorphoPath(control_points=control_points)
            helical_pose_sampler = path_samplers.HelicalPoseSampler(spacing=distance_between_particles, twist=twist)
            helical_poses = helical_pose_sampler.sample(path)
            positions = helical_poses.positions
            orientations = helical_poses.orientations[:, :, 2]
            pose_data = {
                'x': positions[:, -3],
                'y': positions[:, -2],
                'z': positions[:, -1],
                'direction_x': orientations[:, -3],
                'direction_y': orientations[:, -2],
                'direction_z': orientations[:, -1],
                'path_id': [f"{path_id}"] * len(positions),
                'id': [tilt_series_id] * len(positions)
            }
            path_df = pd.DataFrame(pose_data)
            all_dfs.append(path_df)

        final_df = pd.concat(all_dfs)
    starfile.write({"paths": final_df}, output_star_file, overwrite=True)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}')


pose_generation_cli.add_typer(pose_generation_paths_cli)
