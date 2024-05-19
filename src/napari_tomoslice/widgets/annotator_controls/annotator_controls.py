from pathlib import Path

from qtpy.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
)

from napari_tomoslice.widgets.annotator_controls.annotation_directory_selector import AnnotationDirectorySelector
from napari_tomoslice.widgets.annotator_controls.annotator_button_group import AnnotatorButtonGroup
from napari_tomoslice.widgets.annotator_controls.save_annotation_button import SaveAnnotationButton


class AnnotatorControls(QWidget):
    def __init__(self, application, annotation_directory: Path = None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.application = application
        self.setLayout(QVBoxLayout())

        self.annotation_directory_selector = AnnotationDirectorySelector(path=annotation_directory)
        self.annotation_list = QListWidget()
        self.annotator_button_group = AnnotatorButtonGroup(application=application)
        self.save_annotation_button = SaveAnnotationButton(application=application)

        self.layout().addWidget(self.annotation_directory_selector)
        self.layout().addWidget(self.annotation_list)
        self.layout().addWidget(self.annotator_button_group)
        self.layout().addWidget(self.save_annotation_button)

        def _update_slicer_annotation_directory(value: Path):
            application.annotation_directory = value
            self.annotation_directory_selector.line_edit.setText(str(application.annotation_directory))

        self.annotation_directory_selector.path_changed.connect(_update_slicer_annotation_directory)
        self.annotation_list.itemActivated.connect(self.load_annotation)


    def update_file_list(self):
        # clear list
        self.annotation_list.clear()

        # get files for list
        tomogram_filename = self.application.tomogram_file
        annotation_directory = self.application.annotation_directory
        if tomogram_filename is None or annotation_directory is None:
            return
        annotation_files = list(annotation_directory.glob(f"{tomogram_filename.stem}*.star"))

        # add to list
        for file in annotation_files:
            _add_result(self.annotation_list, file)

    def load_annotation(self):
        item = self.annotation_list.currentItem()
        self.application.load_annotation(item.path)


def _add_result(results: QListWidget, file: Path):
    item = QListWidgetItem(file.name)
    item.path = file.absolute()
    results.addItem(item)
