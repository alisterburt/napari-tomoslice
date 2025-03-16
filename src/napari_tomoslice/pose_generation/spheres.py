from pathlib import Path

import starfile
import typer
import pandas as pd

from morphosamplers import Sphere, sphere_samplers
from scipy.spatial.transform import Rotation as R

from .cli import pose_generation_cli
from napari_tomoslice.console import console



@pose_generation_cli.command(name='spheres', no_args_is_help=True,
                             help='generate particle poses from sphere annotations')
def generate_poses_spheres(
    annotations_directory: Path = typer.Option(...),
    output_star_file: Path = typer.Option(...),
    distance_between_particles: float = typer.Option(...),
):
    annotation_files = list(annotations_directory.glob('*_spheres.star'))
    console.log(f'Found {len(annotation_files)} files in {annotations_directory}')
    if len(annotation_files) == 0:
        return

    # empty list to store sphere dataframes
    sphere_dfs = []

    # iterate over files and spheres in each file
    for file in annotation_files:
        df = starfile.read(file)
        tilt_series_id = file.stem.rstrip('_spheres')
        console.log(f'Found {len(df)} particles in {file.name}')
        centers = df[['x', 'y', 'z']].to_numpy()
        radii = df['radius'].to_numpy()
        particle_dfs = []

        for center, radius in zip(centers, radii):
            try:
                particle_df = _generate_pose_df_sphere(center, radius, distance_between_particles, tilt_series_id)
                particle_dfs.append(particle_df)

            except ValueError:
                console.log(f'Could not generate pose for sphere at center {center} in {tilt_series_id}')

        file_df = pd.concat(particle_dfs)
        sphere_dfs.append(file_df)

    # write output to disk
    final_df = pd.concat(sphere_dfs)
    sorted_df = final_df.sort_values('tilt_series_id')
    starfile.write(sorted_df, output_star_file, overwrite=True)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}')
    console.log('Done!', style="bold green")

def _generate_pose_df_sphere(center, radius:float,
                             distance_between_particles:float,
                             tilt_series_id:str)-> pd.DataFrame:
    # create a morphosamplers Sphere object
    sphere = Sphere(center=center, radius=radius)
    # sample poses on the sphere
    pose_sampler = sphere_samplers.PoseSampler(spacing=distance_between_particles)
    poses = pose_sampler.sample(sphere)
    # extract positions and euler angles
    positions = poses.positions
    orientations = poses.orientations
    euler_angles = R.from_matrix(orientations).inv().as_euler('ZYZ', degrees=True)

    # construct dataframe
    pose_data = {
        'x': positions[:, 0],
        'y': positions[:, 1],
        'z': positions[:, 2],
        'rot': euler_angles[:, 0],
        'tilt': euler_angles[:, 1],
        'psi': euler_angles[:, 2],
        'tilt_series_id': [tilt_series_id] * len(positions)
    }
    return pd.DataFrame(pose_data)





