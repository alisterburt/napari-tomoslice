# Annotate

Visualize and interactively annotate geometrical structures in cryo-ET data using [*napari*](https://github.com/napari/napari)

*napari-tomoslice* allows you to quickly annotate

- [Points](points.md#annotate-points)
- [Spheres](spheres.md#annotate-spheres)
- [Paths](paths.md#annotate-paths)
- [Dipoles](dipoles.md#annotate-dipoles)

````
 Usage: napari-tomoslice annotate [OPTIONS]                                                                                                                                                                                                      
                                                                                                                                                                                                                                                 
 interactively annotate geometrical structures                                                                                                                                                                                                   
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --tomogram-directory    -t      PATH                            directory containing tomograms [default: None]                                                                                                                             │
│    --file-pattern          -p      TEXT                            file pattern of tomograms [default: *.mrc]                                                                                                                                 │
│    --annotation-directory  -a      PATH                            directory to save annotations [default: 2025_05_21_19:44:38]                                                                                                               │
│ *  --mode                  -m      [points|paths|spheres|dipoles]  annotation mode [required]                                                                                                                                                 │
│    --help                                                          Show this message and exit.                                                                                                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````

