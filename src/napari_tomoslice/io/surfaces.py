from pathlib import Path

import napari
import numpy as np
import pandas as pd
import starfile
from napari_threedee.data_models import N3dSurface, N3dSurfaces

def load_surfaces(path: Path) -> napari.layers.Points:
    df = starfile.read(path)
    surface_data = [
        N3dSurface(data=[_level_df[['z', 'y', 'x']].to_numpy()
        for name, _level_df in _df.groupby('level_id')])
        for name, _df in df.groupby('surface_id')
    ]
    layer = N3dSurfaces(data=surface_data).as_layer()
    layer.selected_data = {len(layer.data) - 1}
    return layer

def save_surfaces(layer: napari.layers.Points, path: Path):
    surfaces = N3dSurfaces.from_layer(layer)
    if len(surfaces) == 0:
        raise RuntimeError('no surfaces to save')
    pass
    zyx = np.concatenate([surface.data for surface in surfaces])
    surface_data = {
        'level_id': surfaces.level_ids,
        'surface_id': surfaces.surface_ids,
        'x': zyx[:, -1],
        'y': zyx[:, -2],
        'z': zyx[:, -3],
    }
    df = pd.DataFrame(surface_data)
    starfile.write({"surfaces": df}, path, overwrite=True)
