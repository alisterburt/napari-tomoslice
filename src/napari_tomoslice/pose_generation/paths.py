import typer
from pathlib import Path

import starfile
import typer
import pandas as pd
from morphosamplers import Path as mPath, path_samplers

from .cli import pose_generation_cli as pose_generation_cli
from napari_tomoslice.console import console

pose_generation_paths_cli = typer.Typer(name='paths', no_args_is_help=True)


@pose_generation_paths_cli.command(name='backbone')
def generate_poses_paths_backbone(
        annotations_directory: Path = typer.Option(...),
        output_star_file: Path = typer.Option(...),
        distance_between_particles: float = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_paths.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    all_dfs = []
    for file in annotation_files:
        tilt_series_id = file.stem.rstrip('_paths')
        df = starfile.read(file)
        num_paths = df['path_id'].nunique()
        console.log(f'Found {num_paths} paths in {file.name}')
        grouped_paths = df.groupby('path_id')
        for path_id, path_data in grouped_paths:
            control_points = path_data[['x', 'y', 'z']].values
            path = mPath(control_points=control_points)
            pose_sampler = path_samplers.PoseSampler(spacing=distance_between_particles)
            poses = pose_sampler.sample(path)
            positions = poses.positions
            orientations = poses.orientations[:, :, 2]
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
            pose_df = pd.DataFrame(pose_data)
            all_dfs.append(pose_df)
        final_df = pd.concat(all_dfs)
    starfile.write({"paths": final_df}, output_star_file, overwrite=True)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}')


@pose_generation_paths_cli.command(name='rings')
def generate_poses_paths_rings():
    print('coming soon...')


@pose_generation_paths_cli.command(name='helix')
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
            path = mPath(control_points=control_points)
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
            pose_df = pd.DataFrame(pose_data)
            all_dfs.append(pose_df)
        final_df = pd.concat(all_dfs)
    starfile.write({"paths": final_df}, output_star_file, overwrite=True)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}')

pose_generation_cli.add_typer(pose_generation_paths_cli)
