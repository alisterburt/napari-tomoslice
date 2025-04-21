import numpy as np

import warnings

# Filter out DeprecationWarnings and UserWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from napari_threedee.data_models import (
    N3dPoints,
    N3dPath,
    N3dPaths,
    N3dSpheres
)
from napari_tomoslice.io import (
    load_points,
    save_points,
    load_paths,
    save_paths,
    load_spheres,
    save_spheres,
)


def test_points_io(tmp_path):
    xyz = np.random.normal(size=(100, 3))
    layer = N3dPoints(data=xyz).as_layer()

    # there and back
    save_points(layer, tmp_path / "points.star")
    layer_after_save = load_points(tmp_path / "points.star")

    assert np.allclose(layer.data, layer_after_save.data, atol=1e-5)


def test_paths_io(tmp_path):
    xyz = np.random.normal(size=(100, 3))
    path_data = [N3dPath(data=xyz), N3dPath(data=xyz)]
    layer = N3dPaths(data=path_data).as_layer()

    # there and back
    save_paths(layer, tmp_path / "paths.star")
    layer_after_save = load_paths(tmp_path / "paths.star")

    assert np.allclose(layer.data, layer_after_save.data, atol=1e-5)


def test_sphere_io(tmp_path):
    xyz = np.random.normal(size=(100, 3))
    radii = np.random.normal(size=(100,))
    layer = N3dSpheres(centers=xyz, radii=radii).as_layer()

    # there and back
    save_spheres(layer, tmp_path / "spheres.star")
    layer_after_save = load_spheres(tmp_path / "spheres.star")
    assert np.allclose(layer.data, layer_after_save.data, atol=1e-5)

    assert np.allclose(layer.data, layer_after_save.data, atol=1e-5)
