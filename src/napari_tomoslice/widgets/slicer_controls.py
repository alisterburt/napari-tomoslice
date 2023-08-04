from qtpy.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from .tomogram_path_selector import TomogramPathSelectorWidget
from .annotator_button_group import AnnotatorButtonGroup


class SlicerControlsWidget(QWidget):
    def __init__(self, slicer, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.tomogram_selector = TomogramPathSelectorWidget(slicer=slicer, parent=self)
        self.annotator_button_group = AnnotatorButtonGroup(slicer=slicer, parent=self)

        self.layout().addWidget(self.tomogram_selector)
        self.layout().addWidget(self.annotator_button_group)
