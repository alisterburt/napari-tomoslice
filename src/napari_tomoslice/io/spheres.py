from pathlib import Path

import napari
import pandas as pd
import starfile
from napari_threedee.data_models import N3dSpheres


def load_spheres(path: Path) -> napari.layers.Points:
    df = starfile.read(path)
    centers = df[['z', 'y', 'x']].to_numpy()
    radii = df['radius'].to_numpy()
    return N3dSpheres(centers=centers, radii=radii).as_layer()


def save_spheres(layer: napari.layers.Points, path: Path):
    spheres = N3dSpheres.from_layer(layer)
    if len(spheres.centers) == 0:
        raise RuntimeError('no spheres to save')
    sphere_data = {
        'x': spheres.centers[:, -1],
        'y': spheres.centers[:, -2],
        'z': spheres.centers[:, -3],
        'radius': spheres.radii,
    }
    df = pd.DataFrame(sphere_data)
    starfile.write({"points": df}, path, overwrite=True)
