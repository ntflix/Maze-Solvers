from typing import Any, Optional, Tuple
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class LabelledIconButton(QWidget):
    onButtonPressed = pyqtSignal(bool)

    def __init__(
        self,
        icon: QStyle.StandardPixmap,
        labelText: str,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        An icon button with a text label.
        """
        super(LabelledIconButton, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        verticalLayout = QVBoxLayout(self)
        verticalLayout.setContentsMargins(0, 0, 0, 0)

        button = QToolButton(self)
        button.setIcon(
            self.style().standardIcon(icon),
        )

        # connect the button to the onButtonPressed signal
        self.onButtonPressed = button.clicked

        label = QLabel(labelText, self)

        verticalLayout.addWidget(button)
        verticalLayout.addWidget(label)
        verticalLayout.setAlignment(label, Qt.Alignment.AlignHCenter)
        verticalLayout.setAlignment(button, Qt.Alignment.AlignHCenter)

        self.setLayout(verticalLayout)
