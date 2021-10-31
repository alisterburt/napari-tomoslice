import napari.viewer
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QVBoxLayout, QFileDialog


from .open_close_buttons import OpenCloseButtonsWidget
from .named_labeled_slider import NamedLabeledSlider
from .selectable_button_list import LabeledSelectableButtonList
from .utils import enable_with_opacity, disable_with_opacity

from napari_tomoslice.tomoslice import TomoSlice, RenderingMode


class TomoSliceWidget(QWidget):
    def __init__(self, viewer: napari.viewer.Viewer):
        super().__init__()
        self.viewer = viewer
        self.tomoslice = TomoSlice(viewer)

        self.open_close_buttons = OpenCloseButtonsWidget(
            open_button=('open tomogram', self._on_tomogram_open),
            close_button=('close tomogram', self._on_tomogram_close)
        )
        self.plane_volume_toggle = LabeledSelectableButtonList(
            label='render as:',
            button_data=(
                ('volume', self._on_render_as_volume),
                ('plane', self._on_render_as_plane)
            )
        )
        self.plane_volume_toggle.setStyleSheet(
            """QPushButton:pressed {
  background-color: {{ highlight }};
}"""
        )
        self.plane_thickness_controls = NamedLabeledSlider(
            label='thickness:',
            minimum_value=1,
            maximum_value=50,
            default_value=5
        )
        self.plane_thickness_controls.slider.valueChanged.connect(
            self._on_thickness_slider_changed
        )

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.open_close_buttons)
        self.layout().addWidget(self.plane_volume_toggle)
        self.layout().addWidget(self.plane_thickness_controls)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(8, 2, 2, 2)
        self.layout().addStretch(1)

        disable_with_opacity(self.plane_volume_toggle)
        disable_with_opacity(self.plane_thickness_controls)
        self.setFixedHeight(90)

    def _on_tomogram_open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a tomogram file...",
            "",
            "tomogram files (*.mrc)",
            options=options
        )
        if filename == '':  # no file selected, early exit
            return
        self.tomoslice.open_tomogram(filename)
        enable_with_opacity(self.plane_volume_toggle)
        if self.tomoslice.rendering_mode == RenderingMode.VOLUME:
            disable_with_opacity(self.plane_thickness_controls)
        else:
            enable_with_opacity(self.plane_thickness_controls)

    def _on_tomogram_close(self):
        self.tomoslice.close_tomogram()
        disable_with_opacity(self.plane_thickness_controls)
        disable_with_opacity(self.plane_volume_toggle)

    def _on_render_as_volume(self):
        self.tomoslice.rendering_mode = RenderingMode.VOLUME
        disable_with_opacity(self.plane_thickness_controls)

    def _on_render_as_plane(self):
        self.tomoslice.rendering_mode = RenderingMode.PLANE
        enable_with_opacity(self.plane_thickness_controls)

    def _on_thickness_slider_changed(self):
        self.tomoslice.plane_thickness = self.plane_thickness_controls.slider.value()


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    widget_options = {
        "name": "napari-tomoslice",
        "add_vertical_stretch": False,
        "area": 'left',
    }
    return TomoSliceWidget, widget_options
