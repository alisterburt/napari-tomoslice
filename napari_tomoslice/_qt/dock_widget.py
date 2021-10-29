import napari.viewer
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel
from superqt import QLabeledDoubleSlider

from napari_tomoslice.tomoslice import TomoSlice


class TomoSliceWidget(QWidget):
    def __init__(self, viewer: napari.viewer.Viewer):
        super().__init__()
        self.viewer = viewer
        self.tomoslice = TomoSlice(viewer)

        self.setLayout(QVBoxLayout())

        self.button_layout = QHBoxLayout()
        self.open_tomogram_button = QPushButton("open tomogram")
        self.open_tomogram_button.clicked.connect(self._on_tomogram_open)

        self.close_tomogram_button = QPushButton("close tomogram")
        self.close_tomogram_button.clicked.connect(
            self._on_tomogram_close
        )
        self.button_layout.addWidget(self.open_tomogram_button)
        self.button_layout.addWidget(self.close_tomogram_button)

        self.thickness_label = QLabel('thickness:')
        self.thickness_slider = QLabeledDoubleSlider(Qt.Horizontal, parent=self)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(50)
        self.thickness_slider.setValue(5)
        self.thickness_slider.valueChanged.connect(
            self._on_thickness_slider_changed
        )

        self.thickness_slider.hide()
        self.thickness_label.hide()
        self.close_tomogram_button.setDisabled(True)

        self.thickness_row = QHBoxLayout()
        self.thickness_row.addWidget(self.thickness_label)
        self.thickness_row.addWidget(self.thickness_slider)

        self.layout().addLayout(self.button_layout)
        self.layout().addStretch(1)
        self.layout().addLayout(self.thickness_row)

        self.setMaximumHeight(80)
        self.setMaximumWidth(260)

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
        self.update_widget_visibility(tomogram_opened=True)

    def _on_tomogram_close(self):
        self.tomoslice.close_tomogram()
        self.update_widget_visibility(tomogram_opened=False)

    def update_widget_visibility(self, tomogram_opened: bool):
        if tomogram_opened is True:
            self.thickness_label.show()
            self.thickness_slider.show()
            self.open_tomogram_button.setDisabled(True)
            self.close_tomogram_button.setEnabled(True)
        elif tomogram_opened is False:
            self.thickness_label.hide()
            self.thickness_slider.hide()
            self.close_tomogram_button.setDisabled(True)
            self.open_tomogram_button.setEnabled(True)

    def _on_thickness_slider_changed(self):
        self.tomoslice.plane_layer.experimental_slicing_plane.thickness = self.thickness_slider.value()


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    widget_options = {
        "name": "napari-tomoslice",
        "add_vertical_stretch": False,
        "area": 'left',
    }
    return TomoSliceWidget, widget_options
