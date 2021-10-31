from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel
from qtpy.QtCore import Qt
from superqt import QLabeledDoubleSlider


class NamedLabeledSlider(QWidget):
    def __init__(self, label: str, minimum_value: float, maximum_value: float, default_value: float, step: float = 0.01):
        super().__init__()
        self.label = QLabel(label)
        self.slider = QLabeledDoubleSlider(Qt.Horizontal, parent=self)
        self.slider.setMinimum(minimum_value)
        self.slider.setMaximum(maximum_value)
        self.slider.setValue(default_value)
        self.slider.setSingleStep(step)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.slider)
        self.layout().setContentsMargins(2, 2, 2, 2)
