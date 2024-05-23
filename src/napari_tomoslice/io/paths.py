from pathlib import Path

import napari
import numpy as np
import pandas as pd
import starfile
from napari_threedee.data_models import N3dPath, N3dPaths


def load_paths(path: Path) -> napari.layers.Points:
    df = starfile.read(path)
    path_data = [
        N3dPath(data=_df[['z', 'y', 'x']].to_numpy())
        for name, _df
        in df.groupby('path_id')
    ]
    layer = N3dPaths(data=path_data).as_layer()
    layer.selected_data = {len(layer.data) - 1}
    return layer


def save_paths(layer: napari.layers.Points, path: Path):
    paths = N3dPaths.from_layer(layer)
    if len(paths) == 0:
        raise RuntimeError('no filaments to save')
    pass
    zyx = np.concatenate([path.data for path in paths])
    path_data = {
        'path_id': paths.path_ids,
        'x': zyx[:, -1],
        'y': zyx[:, -2],
        'z': zyx[:, -3],
    }
    df = pd.DataFrame(path_data)
    starfile.write({"paths": df}, path, overwrite=True)
