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
│    --tomogram-directory          PATH                            [default: None]                                                                                                                                                              │
│    --file-pattern                TEXT                            [default: *.mrc]                                                                                                                                                             │
│    --annotation-directory        PATH                            [default: 2025_03_11_19:57:13]                                                                                                                                               │
│ *  --mode                        [points|paths|spheres|dipoles]  [required]                                                                                                                                                                   │
│    --help                                                        Show this message and exit.                                                                                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````

