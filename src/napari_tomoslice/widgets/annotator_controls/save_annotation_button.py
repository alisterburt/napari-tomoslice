from qtpy.QtWidgets import QPushButton


class SaveAnnotationButton(QPushButton):
    def __init__(self, application, *args):
        super().__init__('save selected annotation', *args)
        self.slicer = application
        self.clicked.connect(self.slicer.save_annotation)
