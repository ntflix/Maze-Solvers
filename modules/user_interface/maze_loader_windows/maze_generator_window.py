from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6 import QtCore
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QMainWindow, QWidget


class MazeGeneratorWindow(QMainWindow):
    gotMaze = QtCore.pyqtSignal(MazeProtocol)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A window presented to the user prompting them for maze specification.
        """
        super(MazeGeneratorWindow, self).__init__(parent=parent, *args, **kwargs)

        generateMazeView = GenerateMazeGroupView(parent=self)
        generateMazeView.mazeGenerated.connect(self.gotMaze)

        self.setCentralWidget(generateMazeView)

        self.setWindowTitle("Generate a Maze")

        self.show()
