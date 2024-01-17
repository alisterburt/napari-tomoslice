from pathlib import Path

from qtpy.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from .annotation_directory_selector import AnnotationDirectorySelector
from .annotator_button_group import AnnotatorButtonGroup
from .save_annotation_button import SaveAnnotationButton


class AnnotatorControls(QWidget):
    def __init__(self, application, annotation_directory: Path = None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.annotation_directory_selector = AnnotationDirectorySelector(path=annotation_directory)
        self.annotator_button_group = AnnotatorButtonGroup(application=application)
        self.save_annotation_button = SaveAnnotationButton(application=application)

        self.layout().addWidget(self.annotation_directory_selector)
        self.layout().addWidget(self.annotator_button_group)
        self.layout().addWidget(self.save_annotation_button)

        def _update_slicer_annotation_directory(value: Path):
            application.annotation_directory = value
            self.annotation_directory_selector.line_edit.setText(str(application.annotation_directory))

        self.annotation_directory_selector.path_changed.connect(_update_slicer_annotation_directory)
