import platform

CLI_NAME = 'napari-tomoslice'
CONTROLS_WIDGET_NAME = 'tomoslice controls'
FOLDER_BROWSER_WIDGET_NAME = 'browser'
PLATFORM_IS_MACOS = True if platform.system() == "Darwin" else False

# default volume layer parameters
TOMOGRAM_LAYER_NAME = 'tomogram'
PLANE_NORMAL_VECTOR = (1, 0, 0)
PLANE_THICKNESS = 1

# file filters
TOMOGRAM_FILE_FILTER = '*.mrc'

# help text templates
_ALT = "'⌥'" if PLATFORM_IS_MACOS else "'Alt'"

PLANE_CONTROLS_HELP_TEXT = """
- click + drag to reorient the camera
- 'Shift' + click + drag to move the plane
- 'x'/'y'/'z'/'o' to reorient the plane
"""

DISABLED_ANNOTATOR_HELP_TEXT = f"""
- load a tomogram 
- enable an annotator to start annotating
"""

POINT_ANNOTATOR_HELP_TEXT = f"""
- {_ALT} + click to add a new point
"""

PATH_ANNOTATOR_HELP_TEXT = f"""
- 'n' to start a new path
- {_ALT} + click to add a new point to the current path
"""

SPHERE_ANNOTATOR_HELP_TEXT = f"""
- 'n' to start a new sphere
- {_ALT} + click to add the sphere, repeat to move it
- 'r' to change the radius
"""
