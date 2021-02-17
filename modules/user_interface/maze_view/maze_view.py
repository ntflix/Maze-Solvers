from PyQt6.QtCore import QSize
from modules.data_structures.maze.maze import Maze
from modules.user_interface.maze_view.maze_view_painter import MazeViewPainter
from typing import Any
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MazeView(QWidget):
    def __init__(
        self,
        maze: Maze,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super(MazeView, self).__init__(*args, **kwargs)

        # Initialise a painter for use in the frame
        mazeViewPaint = MazeViewPainter(
            size=QSize(400, 400),
            maze=maze,
        )

        layout = QVBoxLayout()
        layout.addWidget(mazeViewPaint)

        self.setLayout(layout)
