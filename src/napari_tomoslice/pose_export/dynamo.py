from pathlib import Path

import pandas as pd
import dynamotable
from scipy.spatial.transform import Rotation as R

from napari_tomoslice.console import console

def convert_poses_dynamo(df: pd.DataFrame, output_file: Path):
    console.log('converting star file into Dynamo compatible output...')
    eulers = df[['rot', 'tilt', 'psi']].to_numpy()
    rotation_matrices = R.from_euler(angles=eulers, seq='ZYZ', degrees=True).inv().as_matrix()
    eulers_dynamo = R.from_matrix(rotation_matrices).inv().as_euler(seq='zxz', degrees=True)
    dynamo_data = {
        'x': df['x'],
        'y': df['y'],
        'z': df['z'],
        'tdrot': eulers_dynamo[:, 0],
        'tilt': eulers_dynamo[:, 1],
        'narot': eulers_dynamo[:, 2],
        'tomo': df['tilt_series_id'],
    }
    if 'manifold_id' in df.columns:
        dynamo_data['reg'] = df['manifold_id']

    dynamo_df = pd.DataFrame(dynamo_data)
    dynamotable.write(dynamo_df, output_file)
    console.log(f'writing {len(df)} particles to {output_file}...')




