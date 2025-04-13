from enum import Enum
from pathlib import Path

import starfile
import typer

from napari_tomoslice.console import console
from .relion5 import convert_poses_relion5
from .dynamo import convert_poses_dynamo


class OutputType(Enum):
    RELION5 = "relion5"
    DYNAMO = 'dynamo'


def pose_convert_cli(
    input_file: Path = typer.Option(...),
    output_type: OutputType = typer.Option(...),
    output_file: Path = typer.Option(...)
) -> None:
    try:
        df = starfile.read(input_file)
        console.log(f'reading {input_file}...')
        console.log(f'read {len(df)} rows from {input_file}')

        if output_type == OutputType.RELION5:
            convert_poses_relion5(df, output_file)
        elif output_type == OutputType.DYNAMO:
            convert_poses_dynamo(df, output_file)
        else:
            raise NotImplementedError(output_type)
        console.log('Done!', style="bold green")

    except Exception as e:
        console.log(f'Error: {str(e)}', style="bold red")
