import platform

TOMOSLICE_CLI_NAME = 'napari-tomoslice'
ANNOTATION_CLI_NAME = 'annotate'
POSE_GENERATION_CLI_NAME = 'generate-poses'
POSE_EXPORT_CLI_NAME = 'convert-poses'
TOMOGRAM_BROWSER_WIDGET_NAME = 'tomogram browser'
ANNOTATION_BROWSER_WIDGET_NAME = 'annotation browser'
PLATFORM_IS_MACOS = True if platform.system() == "Darwin" else False

# default volume layer parameters
TOMOGRAM_LAYER_NAME = 'tomogram'
PLANE_NORMAL_VECTOR = (1, 0, 0)
PLANE_THICKNESS = 1

# default point annotation parameters
POINT_ANNOTATION_FACE_COLOR = 'cornflowerblue'

# help text templates
_ALT = "'⌥'" if PLATFORM_IS_MACOS else "'Alt'"

PLANE_CONTROLS_HELP_TEXT = """
- click + drag to reorient the camera
- Shift + click + drag to move the plane
- x/y/z/o to reorient the plane
"""

DISABLED_ANNOTATOR_HELP_TEXT = f"""
- load a tomogram using the tomogram browser
- start annotating!
"""

POINT_ANNOTATOR_HELP_TEXT = f"""
- {_ALT} + click to add a new point
"""

PATH_ANNOTATOR_HELP_TEXT = f"""
- press 'n' to start a new path
- {_ALT} + click to add a new point to the current path
"""

SPHERE_ANNOTATOR_HELP_TEXT = f"""
- press 'n' to start a new sphere
- {_ALT} + click to set the center of the new sphere
- press 'r' at desired edge of sphere to change the radius
- {_ALT} + click again to move the sphere 
"""

DIPOLE_ANNOTATOR_HELP_TEXT = f"""
- press 'n' to start a new dipole
- {_ALT} + click to set the position of the new dipole
- press 'v' to set the direction of the dipole
- {_ALT} + click again to move the dipole
"""

