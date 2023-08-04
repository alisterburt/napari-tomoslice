from pathlib import Path

import numpy as np
import mrcfile


def read_volume(path: Path) -> np.ndarray:
    """Wrapper potentially capable of reading multiple file types."""
    volume = mrcfile.read(path)
    return volume
