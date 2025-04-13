from pathlib import Path

import pandas as pd
import starfile

from napari_tomoslice.console import console


def convert_poses_relion5(df: pd.DataFrame, output_file: Path):
    console.log('renaming columns for RELION (version 5) compatible output...')
    df.rename(
        columns={
            "x": "rlnCoordinateX",
            "y": "rlnCoordinateY",
            "z": "rlnCoordinateZ",
            "rot": "rlnAngleRot",
            "tilt": "rlnAngleTilt",
            "psi": "rlnAnglePsi",
            "tilt_series_id": "rlnTomoName",
            "manifold_id": "rlnTomoManifoldIndex"
        },
        inplace=True
    )
    console.log(f'writing {len(df)} particles to {output_file}...')
    starfile.write(df, output_file, overwrite=True)

