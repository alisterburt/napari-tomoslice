# napari-tomoslice

[![License](https://img.shields.io/pypi/l/napari-tomoslice.svg?color=green)](https://github.com/alisterburt/napari-tomoslice/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-tomoslice.svg?color=green)](https://pypi.org/project/napari-tomoslice)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-tomoslice.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/napari-tomoslice/actions/workflows/ci.yml/badge.svg)](https://github.com/alisterburt/napari-tomoslice/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/alisterburt/napari-tomoslice/branch/main/graph/badge.svg)](https://codecov.io/gh/alisterburt/napari-tomoslice)

*napari-tomoslice* is a tool for tomogram visualisation and annotation in napari.

## Features

*napari-tomoslice* allows you to quickly annotate
- points
- paths
- spheres

Annotations are saved in the [STAR file format](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval)
and can be easily manipulated in Python using [starfile](https://teamtomo.org/starfile/).

## Installation

*napari-tomoslice* is available on PyPI.

```shell
pip install napari-tomoslice
```

We recommend installing into a fresh virtual environment.

## Usage

```sh
 Usage: napari-tomoslice [OPTIONS]                                                                                                                                              
                                                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --tomogram-directory          PATH                    [default: None]                                                                                                     │
│    --file-pattern                TEXT                    [default: *.mrc]                                                                                                    │
│    --annotation-directory        PATH                    [default: 2024_05_22_21:16:44]                                                                                      │
│ *  --mode                        [points|paths|spheres]  [required]                                                                                                          │
│    --help                                                Show this message and exit.                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````

## Inspiration

*napari-tomoslice* is heavily inspired by [*dtmslice* in Dynamo](https://www.dynamo-em.org/w/index.php?title=Dtmslice).

*napari-tomoslice* is built on 
[*napari*](https://github.com/napari/napari) 
and 
[*napari-threedee*](https://github.com/napari-threedee/napari-threedee).