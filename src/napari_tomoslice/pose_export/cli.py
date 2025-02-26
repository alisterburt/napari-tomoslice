from enum import Enum
from pathlib import Path

import starfile
import typer

from napari_tomoslice.console import console
from .relion5 import export_poses_relion5
from .dynamo import export_poses_dynamo


class OutputType(Enum):
    RELION5 = "relion5"
    DYNAMO = 'dynamo'


def pose_export_cli(
    input_file: Path = typer.Option(...),
    output_type: OutputType = typer.Option(...),
    output_file: Path = typer.Option(...)
) -> None:
    console.log(f'reading {input_file}...')
    df = starfile.read(input_file)
    console.log(f'read {len(df)} rows from {input_file}')

    if output_type == OutputType.RELION5:
        export_poses_relion5(df, output_file)
    if output_type == OutputType.DYNAMO:
        export_poses_dynamo(df, output_file)
    else:
        raise NotImplementedError(output_type)
