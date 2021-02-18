from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtCore import QSize
from modules.user_interface.maze_view.maze_view import MazeView
from typing import Any, Tuple
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)


class MazeViewWindow(QMainWindow):
    def __init__(
        self,
        parent: QWidget,
        maze: MazeProtocol,
        minimumSize: QSize = QSize(500, 500),
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A separate window for displaying a MazeView. No controls.
        """
        super(MazeViewWindow, self).__init__(parent)
        self.setMinimumSize(minimumSize)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            MazeView(
                minimumSize=minimumSize,
                maze=maze,
                parent=self,
                keepAspectRatio=False,
            )
        )

        self.setLayout(layout)
