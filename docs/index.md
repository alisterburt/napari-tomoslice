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

## Installation

    pip install napari-tomoslice


