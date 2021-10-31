from typing import Optional

import napari.layers
import napari.viewer
import numpy as np
from napari.utils.geometry import clamp_point_to_bounding_box

from napari_tomoslice.interactivity_utils import point_in_bounding_box, \
    drag_data_to_projected_distance, point_in_layer_bounding_box


def shift_plane_along_normal(viewer, event, layer: Optional[napari.layers.Image] = None):
    """Shift a rendered plane along its normal vector.
    This function will shift a plane along its normal vector when the plane is
    clicked and dragged."""
    # Calculate intersection of click with plane through data in data coordinates
    intersection = layer.experimental_slicing_plane.intersect_with_line(
        line_position=event.position,
        line_direction=event.view_direction
    )

    # Check if click was on plane by checking if intersection occurs within
    # data bounding box. If not, exit early.
    if not point_in_bounding_box(intersection, layer.extent.data):
        return

    # Store original plane position and disable interactivity during plane drag
    original_plane_position = np.copy(layer.experimental_slicing_plane.position)
    layer.interactive = False

    # Store mouse position at start of drag
    start_position = np.copy(event.position)
    yield

    while event.type == 'mouse_move':
        current_position = event.position
        current_view_direction = event.view_direction
        current_plane_normal = layer.experimental_slicing_plane.normal

        # Project mouse drag onto plane normal
        drag_distance = drag_data_to_projected_distance(
            start_position=start_position,
            end_position=current_position,
            view_direction=current_view_direction,
            vector=current_plane_normal,
        )

        # Calculate updated plane position
        updated_position = original_plane_position + (
                drag_distance * np.array(layer.experimental_slicing_plane.normal)
        )

        clamped_plane_position = clamp_point_to_bounding_box(
            updated_position, layer._display_bounding_box(event.dims_displayed)
        )

        layer.experimental_slicing_plane.position = clamped_plane_position
        yield

    # Re-enable volume_layer interactivity after the drag
    layer.interactive = True


def set_plane_normal_axis(
        viewer: napari.viewer.Viewer,
        layer: napari.layers.Image,
        axis='z'
):
    axis_to_normal = {
        'z': (1, 0, 0),
        'y': (0, 1, 0),
        'x': (0, 0, 1),
    }

    new_plane_position = \
        layer.experimental_slicing_plane.intersect_with_line(
            line_position=viewer.cursor.position,
            line_direction=viewer.camera.view_direction,
        )
    if not point_in_layer_bounding_box(new_plane_position, layer):
        # intersection can fall outside volume_layer bounding box
        new_plane_position = np.array(layer.data.shape) // 2

    layer.experimental_slicing_plane.position = new_plane_position
    layer.experimental_slicing_plane.normal = axis_to_normal[axis]


def orient_plane_perpendicular_to_camera(
        viewer: napari.viewer.Viewer,
        layer: napari.layers.Image
):
    layer.experimental_slicing_plane.position = np.array(layer.data.shape) // 2
    layer.experimental_slicing_plane.normal = viewer.camera.view_direction
