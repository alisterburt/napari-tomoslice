from pathlib import Path
from types import NoneType
from typing import Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
)
from qtpy.QtGui import QFont
from psygnal import Signal

from napari_tomoslice._constants import TOMOGRAM_FILE_FILTER


class TomogramPathSelector(QWidget):
    path: Path | None
    path_changed: Signal = Signal(Path)

    def __init__(self, path: Optional[Path] = None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = Path('./') if path is None else path
        self.setLayout(QHBoxLayout())

        font = QFont()
        font.setPointSize(11)

        self.label = QLabel('tomogram:')
        self.label.setFont(font)

        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignRight)
        self.line_edit.setFont(font)

        self.button = QPushButton('select')
        self.button.setFont(font)
        self.button.clicked.connect(self.showDialog)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.line_edit)
        self.layout().addWidget(self.button)

        self.layout().setContentsMargins(0, 0, 0, 0)

    def showDialog(self):
        file_name, filter = QFileDialog.getOpenFileName(
            self,
            'Select tomogram file',  # caption
            './',  # directory
            filter=TOMOGRAM_FILE_FILTER
        )
        if file_name != '':
            self.path_changed.emit(Path(file_name))
