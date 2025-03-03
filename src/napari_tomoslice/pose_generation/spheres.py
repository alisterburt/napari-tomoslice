from pathlib import Path

import starfile
import typer
import pandas as pd
from morphosamplers import Sphere, sphere_samplers

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
    all_dfs = []
    for file in annotation_files:
        tilt_series_id = file.stem.rstrip('_spheres')
        df = starfile.read(file)
        console.log(f'Found {len(df)} particles in {file.name}')
        centers = df[['x', 'y', 'z']].values
        radii = df['radius'].values
        particle_dfs = []

        for center, radius in zip(centers, radii):
            sphere = Sphere(center=center, radius=radius)
            pose_sampler = sphere_samplers.PoseSampler(spacing=distance_between_particles)
            poses = pose_sampler.sample(sphere)
            positions = poses.positions
            orientations = poses.orientations[:, :, 2]
            pose_data = {
                'x': positions[:, -1],
                'y': positions[:, -2],
                'z': positions[:, -3],
                'direction_x': orientations[:, -1],
                'direction_y': orientations[:, -2],
                'direction_z': orientations[:, -3],
                'id': [tilt_series_id] * len(positions)
            }
            particle_df = pd.DataFrame(pose_data)
            particle_dfs.append(particle_df)
        file_df = pd.concat(particle_dfs)
        all_dfs.append(file_df)
    final_df = pd.concat(all_dfs)
    sorted_df = final_df.sort_values('id')
    starfile.write(sorted_df, output_star_file, overwrite=True)
    console.log(f'Writing {len(final_df)} particles into {output_star_file}')
    console.log('Done!', style="bold green")








