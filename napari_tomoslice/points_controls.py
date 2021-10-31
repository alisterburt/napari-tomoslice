import napari.layers

from .interactivity_utils import point_in_bounding_box


def add_point(viewer, event, volume_layer: napari.layers.Image = None):
    # Early exit if not alt-clicked
    if 'Alt' not in event.modifiers:
        return

    # Check for active points layer
    if not isinstance(viewer.layers.selection.active, napari.layers.Points):
        return
    else:
        points_layer = viewer.layers.selection.active

    # Ensure added points will be visible until plane depth is sorted
    points_layer.blending = 'additive'

    # Early exit if volume_layer isn't visible
    if not volume_layer.visible:
        return

    # Calculate intersection of click with plane through data in data coordinates
    intersection = volume_layer.experimental_slicing_plane.intersect_with_line(
        line_position=viewer.cursor.position, line_direction=viewer.cursor._view_direction
    )

    # Check if click was on plane by checking if intersection occurs within
    # data bounding box. If not, exit early.
    if not point_in_bounding_box(intersection, volume_layer.extent.data):
        return

    # add point
    points_layer.add(intersection)

