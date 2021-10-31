from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout
from .typing import ButtonData
from .utils import change_enabled_with_opacity


class OpenCloseButtonsWidget(QWidget):
    def __init__(self, open_button: ButtonData, close_button: ButtonData):
        super().__init__()
        self.open_button = QPushButton(open_button[0])
        self.close_button = QPushButton(close_button[0])

        self.open: bool = False

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.open_button)
        self.layout().addWidget(self.close_button)
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.open_button.clicked.connect(open_button[1])
        self.open_button.clicked.connect(self.on_open)
        self.close_button.clicked.connect(close_button[1])
        self.close_button.clicked.connect(self.on_close)

        self.on_open_change(opened=self.open)

    def on_open_change(self, opened: bool):
        self.open = opened
        change_enabled_with_opacity(self.close_button, enabled=self.open)
        change_enabled_with_opacity(self.open_button, enabled=(not self.open))

    def on_open(self):
        self.on_open_change(opened=True)

    def on_close(self):
        self.on_open_change(opened=False)