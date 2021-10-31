from ..open_close_buttons import OpenCloseButtonsWidget
from unittest.mock import MagicMock
from qtpy.QtCore import Qt


def test_open_close_widget_behaviour(qtbot):
    open_button_callback = MagicMock()
    close_button_callback = MagicMock()

    widget = OpenCloseButtonsWidget(
        open_button_name='open me',
        open_button_callback=open_button_callback,
        close_button_name='close me',
        close_button_callback=close_button_callback,
    )
    widget.show()
    qtbot.addWidget(widget)
    assert widget.close_button.isEnabled() is False
    assert widget.open_button.isEnabled() is True

    qtbot.mouseClick(widget.open_button, Qt.LeftButton)
    assert widget.open_button.isEnabled() is False
    assert widget.close_button.isEnabled() is True
    open_button_callback.assert_called_once()

    qtbot.mouseClick(widget.close_button, Qt.LeftButton)
    assert widget.close_button.isEnabled() is False
    assert widget.open_button.isEnabled() is True
    close_button_callback.assert_called_once()
