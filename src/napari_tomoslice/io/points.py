from pathlib import Path

import napari
import pandas as pd
import starfile

from napari_threedee.data_models import N3dPoints


def load_points(path: Path) -> napari.layers.Points:
    df = starfile.read(path)
    return N3dPoints(data=df[['z', 'y', 'x']].to_numpy()).as_layer()


def save_points(layer: napari.layers.Points, path: Path):
    zyx = layer.data
    if len(zyx) == 0:
        raise RuntimeError('no particles to save')
    xyz = {
        'x': zyx[:, -1],
        'y': zyx[:, -2],
        'z': zyx[:, -3],
    }
    df = pd.DataFrame(xyz)
    starfile.write({"points": df}, path, overwrite=True)
