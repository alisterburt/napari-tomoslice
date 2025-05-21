# Convert Poses 

Convert poses generated from geometrical annotations to [RELION](https://relion.readthedocs.io/en/release-5.0/) [STAR files](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval) or [Dynamo tables](https://www.dynamo-em.org/w/index.php?title=Main_Page)
````
Usage: napari-tomoslice convert-poses [OPTIONS]                                                                                                                                                                                                  
                                                                                                                                                                                                                                                 
 convert particle poses generated from geometrical annotations                                                                                                                                                                                    
                                                                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --input_file   -i      PATH              input star file name [default: None] [required]                                                                                                                                                   │
│ *  --output_type  -t      [relion5|dynamo]  target format for the conversion [default: None] [required]                                                                                                                                       │
│ *  --output_file  -o      PATH              output file name [default: None] [required]                                                                                                                                                       │
│    --help                                   Show this message and exit.                                                                                                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````


