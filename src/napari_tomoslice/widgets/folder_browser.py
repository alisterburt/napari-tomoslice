"""Folder browsing widget.

Modelled on https://github.com/haesleinhuepf/napari-folder-browser
"""
import os
from pathlib import Path
from typing import List, Optional

from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, \
    QListWidget, QListWidgetItem, QLabel
from qtpy.QtCore import Qt
from psygnal import Signal
from magicgui.widgets import FileEdit
from magicgui.types import FileDialogMode


class MyQLineEdit(QLineEdit):
    keyup = Signal()
    keydown = Signal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.keyup.emit()
            return
        elif event.key() == Qt.Key_Down:
            self.keydown.emit()
            return
        super().keyPressEvent(event)


class FolderBrowser(QWidget):
    directory: Path | None
    glob_pattern: str

    def __init__(
        self,
        slicer,
        directory: Optional[Path] = None,
        glob_pattern: str = '*'
    ):
        super().__init__()
        self.slicer = slicer
        self._directory = directory if directory is not None else Path(os.getcwd())
        self.glob_pattern = glob_pattern

        self.setLayout(QVBoxLayout())

        self.directory_edit_widget = FileEdit(
            mode=FileDialogMode.EXISTING_DIRECTORY,
            value=self.directory
        )

        self.search_field_widget = MyQLineEdit(self.glob_pattern)
        self.results_list_widget = QListWidget()

        self.search_field_container_widget = QWidget()
        self.search_field_container_widget.setLayout(QHBoxLayout())
        self.search_field_container_widget.layout().addWidget(QLabel("Search:"))
        self.search_field_container_widget.layout().addWidget(self.search_field_widget)

        self.layout().addWidget(QLabel("Directory"))
        self.layout().addWidget(self.directory_edit_widget.native)
        self.layout().addWidget(QLabel("File filter"))
        self.layout().addWidget(self.search_field_container_widget)
        self.layout().addWidget(self.results_list_widget)

        self.directory_edit_widget.line_edit.changed.connect(self.on_directory_change)
        self.search_field_widget.keyup.connect(self.on_key_up)
        self.search_field_widget.keydown.connect(self.on_key_down)
        self.search_field_widget.textChanged.connect(self.on_text_changed)
        self.search_field_widget.returnPressed.connect(self.on_item_double_clicked)
        self.results_list_widget.itemActivated.connect(self.on_item_double_clicked)

        self.on_directory_change()

    @property
    def files(self) -> List[Path]:
        if self.search_field_widget.text() == '':
            glob_pattern = '*'
        else:
            glob_pattern = self.search_field_widget.text()
        files = Path(self.directory).glob(glob_pattern)
        files = [f for f in files if f.is_file()]
        return sorted(list(files))

    @property
    def directory(self) -> Path:
        return self._directory

    @directory.setter
    def directory(self, value: os.PathLike):
        self._directory = Path(value)
        self.on_directory_change()

    def on_directory_change(self, *args, **kwargs):
        self._directory = self.directory_edit_widget.value
        self.on_text_changed()

    def on_text_changed(self, *args, **kwargs):
        self.results_list_widget.clear()
        for file in self.files:
            _add_result(self.results_list_widget, str(file.name))

    def on_key_up(self):
        if self.results_list_widget.currentRow() > 0:
            current_row_idx = self.results_list_widget.currentRow()
            self.results_list_widget.setCurrentRow(current_row_idx - 1)

    def on_key_down(self):
        n_rows = self.results_list_widget.count()
        if self.results_list_widget.currentRow() < n_rows - 1:
            current_row_idx = self.results_list_widget.currentRow()
            self.results_list_widget.setCurrentRow(current_row_idx + 1)

    def on_item_double_clicked(self):
        item = self.results_list_widget.currentItem()
        tomogram_file = self.directory / item.file_name
        self.slicer.tomogram_file = tomogram_file


def _add_result(results: QListWidget, file_name: str):
    item = QListWidgetItem(file_name)
    item.file_name = file_name
    results.addItem(item)
