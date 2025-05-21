# Generate Poses 

Generate poses from geometrical annotations

    napari-tomoslice generate-poses [OPTIONS] COMMAND [ARGS]...   

Poses can be sampled in a number of ways from each annotation type:

- [Points](points.md#generate-poses-from-point-annotations)
- [Spheres](spheres.md#generate-poses-from-sphere-annotations)
- [Path](paths.md#generate-poses-from-path-annotations): [Backbone](paths.md#backbone), [Helix](paths.md#helix), [Rings](paths.md#rings)
- [Dipoles](dipoles.md#generate-poses-from-dipole-annotations): [Direct](dipoles.md#direct-dipole), [Disk](dipoles.md#disk-dipole)

## Points
````
 Usage: napari-tomoslice generate-poses points [OPTIONS]                                                                                                                                                                                         
                                                                                                                                                                                                                                                 
 generate particle poses from point annotations                                                                                                                                                                                                  
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory  -a      PATH  directory containing annotations [default: None] [required]                                                                                                                                          │
│ *  --output-star-file      -o      PATH  output star file name [default: None] [required]                                                                                                                                                     │
│    --help                                Show this message and exit.                                                                                                                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````
 

## Spheres
````
 Usage: napari-tomoslice generate-poses spheres [OPTIONS]                                                                                                                                                                                        
                                                                                                                                                                                                                                                 
 generate particle poses from sphere annotations                                                                                                                                                                                                 
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory        -a      PATH   directory containing annotations [default: None] [required]                                                                                                                                   │
│ *  --output-star-file            -o      PATH   output star file name [default: None] [required]                                                                                                                                              │
│ *  --distance_between_particles  -d      FLOAT  distance between particles on the sphere [default: None] [required]                                                                                                                           │
│    --help                                       Show this message and exit.                                                                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````

## Paths

    napari-tomoslice generate-poses paths [OPTIONS] COMMAND [ARGS]...  

### Backbone
````
 Usage: napari-tomoslice generate-poses paths backbone [OPTIONS]                                                                                                                                                                                 
                                                                                                                                                                                                                                                 
 evenly spaced particle poses along the annotated path                                                                                                                                                                                           
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory        -a      PATH   directory containing annotations [default: None] [required]                                                                                                                                   │
│ *  --output-star-file            -o      PATH   output star file name [default: None] [required]                                                                                                                                              │
│ *  --distance_between_particles  -d      FLOAT  distance between particles along the backbone [default: None] [required]                                                                                                                      │
│    --help                                       Show this message and exit.                                                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````
 
### Helix
````
 Usage: napari-tomoslice generate-poses paths helix [OPTIONS]                                                                                                                                                                                    
                                                                                                                                                                                                                                                 
 evenly spaced particle poses along the annotated helical path                                                                                                                                                                                   
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory        -a      PATH   directory containing annotations [default: None] [required]                                                                                                                                   │
│ *  --output-star-file            -o      PATH   output star file name [default: None] [required]                                                                                                                                              │
│ *  --distance_between_particles  -d      FLOAT  distance between particles along the backbone [default: None] [required]                                                                                                                      │
│ *  --twist                       -t      FLOAT  helical twist [default: None] [required]                                                                                                                                                      │
│    --help                                       Show this message and exit.                                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````


### Rings
````
 Usage: napari-tomoslice generate-poses paths rings [OPTIONS]                                                                                                                                                                                    
                                                                                                                                                                                                                                                 
 particle poses on evenly spaced rings along the annotated path                                                                                                                                                                                  
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory        -a      PATH     directory containing annotations [default: None] [required]                                                                                                                                 │
│ *  --output-star-file            -o      PATH     output star file name [default: None] [required]                                                                                                                                            │
│ *  --distance_between_particles  -d      FLOAT    distance between rings along the backbone [default: None] [required]                                                                                                                        │
│ *  --number_of_points_per_ring   -n      INTEGER  number of particles to be placed on each ring [default: None] [required]                                                                                                                    │
│ *  --ring_radius                 -r      FLOAT    radius of the ring [default: None] [required]                                                                                                                                               │
│    --help                                         Show this message and exit.                                                                                                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````
  

## Dipoles
    napari-tomoslice generate-poses dipoles [OPTIONS] COMMAND [ARGS]...   

### Direct
````
 Usage: napari-tomoslice generate-poses dipoles direct [OPTIONS]                                                                                                                                                                                 
                                                                                                                                                                                                                                                 
 particle poses directly from the annotated dipoles                                                                                                                                                                                              
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory  -a      PATH  directory containing annotations [default: None] [required]                                                                                                                                          │
│ *  --output-star-file      -o      PATH  output star file name [default: None] [required]                                                                                                                                                     │
│    --help                                Show this message and exit.                                                                                                                                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````

### Disk
````
 Usage: napari-tomoslice generate-poses dipoles disk [OPTIONS]                                                                                                                                                                                   
                                                                                                                                                                                                                                                 
 particle poses on a disk around the annotated dipoles                                                                                                                                                                                           
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --annotation-directory        -a      PATH   directory containing annotations [default: None] [required]                                                                                                                                   │
│ *  --output-star-file            -o      PATH   output star file name [default: None] [required]                                                                                                                                              │
│ *  --distance_between_particles  -d      FLOAT  distance between particles on the disk [default: None] [required]                                                                                                                             │
│ *  --disk_radius                 -r      FLOAT  radius of the disk [default: None] [required]                                                                                                                                                 │
│    --help                                       Show this message and exit.                                                                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````