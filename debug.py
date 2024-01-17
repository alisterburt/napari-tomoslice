from napari_tomoslice.main import napari_tomoslice
from pathlib import Path

napari_tomoslice(
    tomogram_file=Path('/Users/burta2/Downloads/1fab_mask.mrc'),
    tomogram_directory=Path('/Users/burta2/Downloads/'),
    tomogram_glob_pattern='*.bla'
)