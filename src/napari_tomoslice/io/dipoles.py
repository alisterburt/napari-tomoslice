from pathlib import Path

import napari
import pandas as pd
import numpy as np
import starfile
from napari_threedee.data_models import N3dDipoles


def load_dipoles(path: Path) -> napari.layers.Points:
    df = starfile.read(path)
    centers = df[['z', 'y', 'x']].to_numpy()
    direction_z = df['direction_z'].to_numpy()
    direction_y = df['direction_y'].to_numpy()
    direction_x = df['direction_x'].to_numpy()
    directions = np.stack([direction_z, direction_y, direction_x], axis=-1)
    layer = N3dDipoles.from_centers_and_directions(centers, directions).as_layer()
    return layer


def save_dipoles(layer: napari.layers.Points, path: Path):
    dipoles = N3dDipoles.from_layer(layer)
    if len(dipoles.centers) == 0:
        raise RuntimeError('no dipoles to save')
    dipoles_data = {
        'x': dipoles.centers[:, -1],
        'y': dipoles.centers[:, -2],
        'z': dipoles.centers[:, -3],
        'direction_x': dipoles.directions[:, -1],
        'direction_y': dipoles.directions[:, -2],
        'direction_z': dipoles.directions[:, -3],
    }
    df = pd.DataFrame(dipoles_data)
    starfile.write({"dipoles": df}, path, overwrite=True)
