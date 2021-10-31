from qtpy.QtWidgets import QWidget, QGraphicsOpacityEffect


def change_enabled_with_opacity(widget: QWidget, enabled: bool):
    """Set enabled state on a QWidget and decrease opacity if not enabled."""
    widget.setEnabled(enabled)
    opacity = QGraphicsOpacityEffect(widget)
    opacity.setOpacity(1 if enabled else 0.5)
    widget.setGraphicsEffect(opacity)


def disable_with_opacity(widget: QWidget):
    change_enabled_with_opacity(widget, enabled=False)


def enable_with_opacity(widget: QWidget):
    change_enabled_with_opacity(widget, enabled=True)