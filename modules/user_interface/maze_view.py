from typing import Any
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget


class MazeView(QWidget):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super(MazeView, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton(parent=None, text="Hello"))
        self.setLayout(layout)
