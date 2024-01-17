from qtpy.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from qtpy.QtGui import QFont


class AnnotatorButtonGroup(QWidget):
    def __init__(self, application, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.slicer = application
        self.setLayout(QHBoxLayout())
        font = QFont()
        font.setPointSize(11)

        self.label = QLabel('annotation mode:')
        self.label.setFont(font)
        self.point_button = QPushButton('point')
        self.path_button = QPushButton('path')
        self.sphere_button = QPushButton('sphere')

        self.buttons = (
            self.point_button,
            self.path_button,
            self.sphere_button
        )

        self.layout().addWidget(self.label)
        for button in self:
            self.layout().addWidget(button)
            button.setCheckable(True)
            button.setFont(font)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.point_button.clicked.connect(self.on_point_button_clicked)
        self.path_button.clicked.connect(self.on_path_button_clicked)
        self.sphere_button.clicked.connect(self.on_sphere_button_clicked)

    def on_point_button_clicked(self):
        from napari_tomoslice.tomoslice import AnnotationMode
        if self.point_button.isChecked():
            self.slicer.annotation_mode = AnnotationMode.POINT
        else:
            self.slicer.annotation_mode = AnnotationMode.DISABLED

    def on_path_button_clicked(self):
        from napari_tomoslice.tomoslice import AnnotationMode
        if self.path_button.isChecked():
            self.slicer.annotation_mode = AnnotationMode.PATH
        else:
            self.slicer.annotation_mode = AnnotationMode.DISABLED

    def on_sphere_button_clicked(self):
        from napari_tomoslice.tomoslice import AnnotationMode
        if self.sphere_button.isChecked():
            self.slicer.annotation_mode = AnnotationMode.SPHERE
        else:
            self.slicer.annotation_mode = AnnotationMode.DISABLED

    def __iter__(self):
        yield from self.buttons
