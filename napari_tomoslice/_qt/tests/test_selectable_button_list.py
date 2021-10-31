import sys
from functools import partial
from typing import Callable, Tuple, Sequence, Optional
from unittest.mock import MagicMock

import napari
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from ..selectable_button_list import LabeledSelectableButtonList


def test_selectable_button_list_instantiation(qtbot):
    button_1_callack = MagicMock()
    button_2_callback = MagicMock()
    widget = LabeledSelectableButtonList([
        ('button 1', button_1_callack),
        ('button 2', button_2_callback)
    ], label='label')
    widget.show()
    assert isinstance(widget, LabeledSelectableButtonList)


def test_selectable_button_list_behaviour(qtbot):
    button_1_callack = MagicMock()
    button_2_callback = MagicMock()
    widget = LabeledSelectableButtonList([
        ('button 1', button_1_callack),
        ('button 2', button_2_callback)
    ], label='label')

    widget.show()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.buttons[0], Qt.LeftButton)
    assert widget.buttons[0].isChecked()
    assert widget.buttons[1].isChecked() is not True
    button_1_callack.assert_called_once()

    qtbot.mouseClick(widget.buttons[1], Qt.LeftButton)
    assert widget.buttons[0].isChecked() is not True
    assert widget.buttons[1].isChecked()
    button_2_callback.assert_called_once()

    for _ in range(5):
        qtbot.mouseClick(widget.buttons[0], Qt.LeftButton)
        assert widget.buttons[0].isChecked()
        assert widget.buttons[1].isChecked() is not True
