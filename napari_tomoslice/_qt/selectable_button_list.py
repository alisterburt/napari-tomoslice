from functools import partial

from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from typing import Callable, Tuple, Sequence, Optional


class LabeledSelectableButtonList(QWidget):
    def __init__(self, button_data: Sequence[Tuple[str, Optional[Callable]]], label: Optional[str]):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = label
        if label:
            self.layout().addWidget(QLabel(label))
        self.buttons = [QPushButton(b[0]) for b in button_data]
        self.callbacks = [b[1] for b in button_data]

        for button, callback in zip(self.buttons, self.callbacks):
            button.setCheckable(True)
            self.layout().addWidget(button)
            if callback is not None:
                button.clicked.connect(callback)
            button.clicked.connect(
                partial(self.set_selected, button=button)
            )

    def set_selected(self, button: QPushButton):
        button.setChecked(True)
        for b in self.buttons:
            if b is not button:
                b.setChecked(False)
