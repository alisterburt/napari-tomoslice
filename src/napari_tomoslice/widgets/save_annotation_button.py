from qtpy.QtWidgets import QPushButton


class SaveAnnotationButton(QPushButton):
    def __init__(self, slicer, *args):
        super().__init__('save selected annotation', *args)
        self.slicer = slicer
        self.clicked.connect(self.slicer.save_annotation)
