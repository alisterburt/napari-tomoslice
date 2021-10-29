from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout
from typing import Callable
from .utils import change_enabled_with_opacity


class OpenCloseButtonsWidget(QWidget):
    def __init__(self, open_button_name: str, close_button_name: str, open_button_callback: Callable, close_button_callback: Callable):
        super().__init__()
        self.open_button = QPushButton(open_button_name)
        self.close_button = QPushButton(close_button_name)

        self.open: bool = False

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.open_button)
        self.layout().addWidget(self.close_button)

        self.open_button.clicked.connect(open_button_callback)
        self.open_button.clicked.connect(self.on_open)
        self.close_button.clicked.connect(close_button_callback)
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