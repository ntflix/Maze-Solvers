from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MazeViewControlsView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(GenerateMazeGroupView(self))
