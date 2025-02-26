from pathlib import Path

import pandas as pd
import dynamotable
from eulerangles import convert_eulers

from napari_tomoslice.console import console

def export_poses_dynamo(df: pd.DataFrame, output_file: Path):
    console.log('converting star file into Dynamo compatible output')
    eulers = df[['rot', 'tilt', 'psi']].to_numpy()
    eulers_dynamo = convert_eulers(eulers, source_meta='relion', target_meta='dynamo')
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
    console.log('done!')




