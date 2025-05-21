# Overview

*napari-tomoslice* is a tool for interactively annotating geometrical structures in cryo-ET data 
and generating particle poses from these geometrical annotations for subtomogram averaging.

With *napari-tomoslice* you can

- [**Annotate**](annotate.md) geometrical structures in [*napari*](https://github.com/napari/napari)
- [**Generate poses**](generate.md) from the geometrical annotations 
- [**Convert poses**](export.md) for your favourite subtomogram averaging package

 *napari-tomoslice* allows you to annotate points, spheres, paths and dipoles. 
 Poses can be sampled in a number of ways from each annotation type, for a complete list see: 
 [pose generation](generate.md)

Poses can be easily converted into [Relion](https://relion.readthedocs.io/en/release-5.0/) [STAR file format](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval) or [Dynamo table format](https://www.dynamo-em.org/w/index.php?title=Main_Page)

## Running *napari-tomoslice* 

*napari-tomoslice* can simply be run using [*uvx*](https://github.com/astral-sh/uv) with:

    uvx napari-tomoslice

[*uv*](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) can be installed with: 

    curl -LsSf https://astral.sh/uv/install.sh | sh

!!! question "How to install and use uv ?"
    More detailed information on [*how to install uv*](https://docs.astral.sh/uv/getting-started/installation/) and [*how to use uvx*](https://docs.astral.sh/uv/guides/tools/) can be found on the [*uv documentation*](https://docs.astral.sh/uv/getting-started/).


## Examples

- [Points](points.md)
- [Spheres](spheres.md)
- [Path](paths.md): [Backbone](paths.md), [Helix](paths.md), [Rings](paths.md)
- [Dipoles](dipoles.md): [Direct](dipoles.md), [Disk](dipoles.md)


### Example Data
Data used in the examples can be downloaded from [*zenodo*](https://zenodo.org/records/15259792)

### Visualize the results 

Results from generate-poses and convert-poses can be visualized with their corresponding tomogram with the example script below:


    # /// script
    # dependencies = [
    #   "mrcfile",
    #   "starfile",
    #   "napari[pyqt5]",
    #   "numpy",
    #   "scipy",
    # ]
    # ///
    import mrcfile
    import napari
    import numpy as np
    import starfile
    from scipy.spatial.transform import Rotation as R

    tomogram_file = 'tomograms/microtubule.mrc'
    particles_file = 'tomograms/backbone.star' # STAR file output from generate-poses or convert-poses
    
    with mrcfile.open(tomogram_file) as mrc:
        tomogram = mrc.data.copy()
    df = starfile.read(particles_file)
    
    xyz = df[['x', 'y', 'z']].to_numpy()
    # xyz_relion = df[['rlnCoordinateX', 'rlnCoordinateY', 'rlnCoordinateZ']].to_numpy()
    
    euler_angles = df[['rot', 'tilt', 'psi']].to_numpy()
    # euler_angles_relion = df[['rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']].to_numpy()
    
    rotations = R.from_euler(seq='ZYZ', angles=euler_angles, degrees=True).inv()
    rotated_z_vectors = rotations.apply([0, 0, 1])
    
    viewer = napari.Viewer(ndisplay=3)
    
    vectors = np.zeros((rotated_z_vectors.shape[0], 2, 3))
    
    vectors[:, 0, :] = xyz[:, ::-1]
    vectors[:, 1, :] = rotated_z_vectors[:, ::-1]
    
    viewer.add_image(tomogram, blending='translucent_no_depth', colormap='gray_r')
    viewer.add_points(xyz[:, ::-1], face_color='cornflowerblue', size=10)
    viewer.add_vectors(vectors, length=12, edge_color='orange', edge_width=4)
    
    napari.run()


