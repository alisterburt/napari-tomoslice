from pathlib import Path
from typing import Optional, List

from psygnal import Signal
from qtpy.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem


class AnnotationList(QWidget):
    annotation_directory: Path | None
    tomogram_filename: Path | None

    def __init__(
        self,
        application,
        annotation_directory: Optional[Path] = None,
        tomogram_filename: Optional[str] = None,
    ):
        super().__init__()
        self.tomoslice = application
        self._annotation_directory = annotation_directory
        self._tomogram_filename = tomogram_filename

        self.setLayout(QVBoxLayout())

        self.annotation_list_widget = QListWidget()
        self.layout().addWidget(self.annotation_list_widget)

        self.annotation_list_widget.itemActivated.connect(self.load_annotation)

        self.update_file_list()


