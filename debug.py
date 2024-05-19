from napari_tomoslice.cli import napari_tomoslice
from pathlib import Path

napari_tomoslice(
    tomogram_file=None,
    tomogram_directory=Path('/Users/burta2/Downloads/'),
    tomogram_glob_pattern='*.mrc',
    annotation_directory='annotation_test',
    mode='paths',
)