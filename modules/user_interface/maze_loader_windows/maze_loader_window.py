from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6 import QtCore
from modules.user_interface.maze_loader_windows.maze_loader_view import MazeLoaderView
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QMainWindow, QWidget


class MazeLoaderWindow(QMainWindow):
    DEFAULT_MAZE_SAVE_PATH = "saves/last_maze.maze"
    gotMaze = QtCore.pyqtSignal(MazeProtocol)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A window presented to the user for either loading or generating a maze.
        """
        super(MazeLoaderWindow, self).__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle("Load a Maze")
        self.setFixedSize(171, 128)

        mazeLoaderChildView = MazeLoaderView(
            lastSaveMazePath=self.DEFAULT_MAZE_SAVE_PATH,
        )

        # connect the gotMaze signal to this signal
        mazeLoaderChildView.gotMaze.connect(self.gotMaze)

        self.setCentralWidget(mazeLoaderChildView)

        self.show()
