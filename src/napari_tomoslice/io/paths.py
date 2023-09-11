from pathlib import Path

import napari
import numpy as np
import pandas as pd
import starfile
from napari_threedee.data_models import N3dPaths


def save_paths(layer: napari.layers.Points, path: Path):
    paths = N3dPaths.from_layer(layer)
    if len(paths) == 0:
        raise RuntimeError('no filaments to save')
    pass
    zyx = np.concatenate([path.data for path in paths])
    filament_data = {
        'filament': paths.spline_ids,
        'x': zyx[:, -1],
        'y': zyx[:, -2],
        'z': zyx[:, -3],
    }
    df = pd.DataFrame(filament_data)
    starfile.write(df, path, overwrite=True)