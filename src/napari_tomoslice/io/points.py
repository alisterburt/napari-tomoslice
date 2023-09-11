from pathlib import Path

import napari
import pandas as pd
import starfile


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
    starfile.write(df, path, overwrite=True)
