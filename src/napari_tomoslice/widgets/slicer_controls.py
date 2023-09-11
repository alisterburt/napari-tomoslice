from pathlib import Path

from qtpy.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from .tomogram_path_selector import TomogramPathSelector
from .output_folder_selector import OutputFolderSelector
from .annotator_button_group import AnnotatorButtonGroup
from .save_annotation_button import SaveAnnotationButton


class SlicerControls(QWidget):
    def __init__(self, slicer, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setLayout(QVBoxLayout())

        self.tomogram_selector = TomogramPathSelector(path=slicer.tomogram_file)
        self.output_folder_selector = OutputFolderSelector(path=slicer.output_folder)
        self.annotator_button_group = AnnotatorButtonGroup(slicer=slicer)
        self.save_annotation_button = SaveAnnotationButton(slicer=slicer)

        self.layout().addWidget(self.tomogram_selector)
        self.layout().addWidget(self.output_folder_selector)
        self.layout().addWidget(self.annotator_button_group)
        self.layout().addWidget(self.save_annotation_button)

        def _update_tomogram_file(value: Path):
            slicer.tomogram_file = value
            self.tomogram_selector.line_edit.setText(str(slicer.tomogram_file))

        def _update_slicer_output_folder(value: Path):
            slicer.output_folder = value
            self.output_folder_selector.line_edit.setText(str(slicer.output_folder))

        self.output_folder_selector.path_changed.connect(_update_slicer_output_folder)
        self.tomogram_selector.path_changed.connect(_update_tomogram_file)
