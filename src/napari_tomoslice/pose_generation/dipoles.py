from pathlib import Path

import starfile
import typer
import pandas as pd


from morphosamplers import Dipole, dipole_samplers
from scipy.spatial.transform import Rotation as R

from napari_tomoslice.console import console
from .cli import pose_generation_cli as pose_generation_cli


pose_generation_dipoles_cli = typer.Typer(name='dipoles', no_args_is_help=True)


@pose_generation_dipoles_cli.command(name='direct')
def generate_poses_dipoles_direct(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_dipoles.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    if len(annotation_files) == 0:
        return

    # empty list to store dipole dataframes
    dipole_dfs = []

    # iterate over files and generate particle poses
    for file in annotation_files:
        df = starfile.read(file)
        tilt_series_id = file.stem.rstrip('_dipoles')
        console.log(f'Found {len(df)} dipoles in {file.name}')
        centers = df[['x', 'y', 'z']].values
        directions = df[['direction_x', 'direction_y', 'direction_z']].values

        for center, direction in zip(centers, directions):
            # create a morphosamplers Dipole object
            dipole = Dipole(center=center, direction=direction)
            pose_sampler = dipole_samplers.PoseSampler()
            poses = pose_sampler.sample(dipole)

            # extract positions and euler angles
            positions = poses.positions
            euler_angles = (R.from_matrix(poses.orientations)
                            .inv()
                            .as_euler(seq='ZYZ', degrees=True)
            )
            # prepare dataframe for output
            particle_pose_data = {
                'x': positions[:, 0],
                'y': positions[:, 1],
                'z': positions[:, 2],
                'rot': euler_angles[:, 0],
                'tilt': euler_angles[:, 1],
                'psi': euler_angles[:, 2],
                'tilt_series_id': [tilt_series_id] * len(positions)
            }
            dipole_df = pd.DataFrame(particle_pose_data)
            dipole_dfs.append(dipole_df)

        console.log(f'Generated {len(dipole_df)} particles for {tilt_series_id}')

    # write all collected data to the output file
    df_out = pd.concat(dipole_dfs)
    console.log(f'Writing {len(df_out)} particles into {output_star_file}...')
    starfile.write({"particles": df_out}, output_star_file, overwrite=True)
    console.log('Done!')



@pose_generation_dipoles_cli.command(name='disk')
def generate_poses_dipoles_disk(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
    distance_between_particles: float = typer.Option(...),
    disk_radius: float = typer.Option(...)
):
    annotation_files = list(annotations_directory.glob('*_dipoles.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    if len(annotation_files) == 0:
        return

    # empty list to store dipole dataframes
    dipole_dfs = []

    # iterate over files and generate particle poses
    for file in annotation_files:
        df = starfile.read(file)
        tilt_series_id = file.stem.rstrip('_dipoles')
        console.log(f'Found {len(df)} dipoles in {file.name}')
        centers = df[['x', 'y', 'z']].values
        directions = df[['direction_x', 'direction_y', 'direction_z']].values

        for center, direction in zip(centers, directions):
            # create a morphosamplers Dipole object
            dipole = Dipole(center=center, direction=direction)
            # create disk points
            disk_sampler = dipole_samplers.DiskSampler(spacing=distance_between_particles, radius=disk_radius)
            final_points = disk_sampler.sample(dipole)

            # create poses for all the disk points
            poses = []
            for point in final_points:
                disk_dipole = Dipole(center=point, direction=direction)
                pose_sampler = dipole_samplers.PoseSampler()
                pose = pose_sampler.sample(disk_dipole)
                poses.append(pose)

            # extract positions and euler angles
            for pose in poses:
                positions = pose.positions
                orientations = pose.orientations
                euler_angles = (R.from_matrix(orientations)
                                .inv()
                                .as_euler(seq='ZYZ', degrees=True)
                )

                particle_pose_data = {
                    'x': positions[:, -3],
                    'y': positions[:, -2],
                    'z': positions[:, -1],
                    'rot': euler_angles[:, 0],
                    'tilt': euler_angles[:, 1],
                    'psi': euler_angles[:, 2],
                    'tilt_series_id': [tilt_series_id] * len(positions)
                }
                dipole_df = pd.DataFrame(particle_pose_data)
                dipole_dfs.append(dipole_df)

        console.log(f'Generated {len(dipole_df)} particles for {tilt_series_id}')

    # write all collected data to the output file
    df_out = pd.concat(dipole_dfs)
    console.log(f'Writing {len(df_out)} particles into {output_star_file}...')
    starfile.write({"particles": df_out}, output_star_file, overwrite=True)
    console.log('Done!')


pose_generation_cli.add_typer(pose_generation_dipoles_cli)
