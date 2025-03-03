from pathlib import Path

import starfile
import typer
import pandas as pd


from morphosamplers import Dipole, dipole_samplers
from scipy.spatial.transform import Rotation as R

from napari_tomoslice.console import console
from napari_tomoslice.pose_generation.cli import pose_generation_cli as pose_generation_cli
from .cli import pose_generation_dipoles_cli as pose_generation_dipoles_cli


@pose_generation_dipoles_cli.command(name='disk', no_args_is_help=True,
                                     help='particle poses on a disk around the annotated dipoles')
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
        for index, (center, direction) in enumerate(zip(centers, directions), start=1):
            try:
                dipole_df = _generate_pose_df_disk(center=center, direction=direction,
                            spacing=distance_between_particles,
                            radius=disk_radius,
                            tilt_series_id=tilt_series_id
                )
                dipole_dfs.append(dipole_df)
                console.log(f'Generated {len(dipole_df)} particles for dipole {index} in {tilt_series_id}')
            except ValueError:
                console.log(f'Could not generate pose for dipoles in {tilt_series_id}')

    # write data to output file
    df_out = pd.concat(dipole_dfs)
    console.log(f'Writing {len(df_out)} particles into {output_star_file}...')
    starfile.write({"particles": df_out}, output_star_file, overwrite=True)
    console.log('Done!', style="bold green")

def _generate_pose_df_disk(center, direction,
                           spacing:float,
                           radius:float,
                           tilt_series_id:str)-> pd.DataFrame:
    # create a morphosamplers Dipole object
    dipole = Dipole(center=center, direction=direction)
    # create disk points
    disk_sampler = dipole_samplers.DiskSampler(spacing=spacing, radius=radius)
    final_points = disk_sampler.sample(dipole)

    # create and save poses for all the disk points
    poses = []
    disk_pose_data = []
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
        for pos, angle in zip(positions, euler_angles):
            disk_pose_data.append({
                'x': pos[0],
                'y': pos[1],
                'z': pos[2],
                'rot': angle[0],
                'tilt': angle[1],
                'psi': angle[2],
                'tilt_series_id': tilt_series_id
            })
    return pd.DataFrame(disk_pose_data)


pose_generation_cli.add_typer(pose_generation_dipoles_cli)
