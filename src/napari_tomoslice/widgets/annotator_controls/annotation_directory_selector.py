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


class AnnotationDirectorySelector(QWidget):
    path: Path | None
    path_changed: Signal = Signal(Path)

    def __init__(self, path: Optional[Path] = None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.path = Path('../') if path is None else path
        self.setLayout(QHBoxLayout())

        font = QFont()
        font.setPointSize(11)

        self.label = QLabel('annotation directory:')
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
        file_name = QFileDialog.getExistingDirectory(
            self,
            'Select output folder',  # caption
            str(self.path),  # directory
        )
        if file_name != '':
            self.path_changed.emit(Path(file_name))
