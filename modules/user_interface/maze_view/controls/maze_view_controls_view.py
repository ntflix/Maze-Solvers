from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class MazeViewControlsView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.addWidget(QPushButton("Epical"))
