from PyQt6.QtGui import QAction, QKeySequence
from modules.user_interface.maze_view.maze_view_controller import MazeViewController
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QWidget,
)


class MazeViewWindow(QMainWindow):
    def __init__(
        self,
        maze: MazeProtocol,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A MazeView with controls.
        """
        super(MazeViewWindow, self).__init__(parent)

        mazeViewController = MazeViewController(
            maze=maze,
            parent=self,
            *args,
            **kwargs,
        )

        self.setMenuBar(self.__getMenuBar())
        self.setCentralWidget(mazeViewController)

    def __getMenuBar(self) -> QMenuBar:
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.addAction("New")

        save = QAction("Save", self)
        save.setShortcut(QKeySequence.StandardKey.Save)
        file.addAction(save)

        edit = bar.addMenu("Edit")
        edit.addAction("copy")
        edit.addAction("paste")

        quit = QAction("Quit", self)
        file.addAction(quit)

        file.triggered.connect(  # type: ignore
            lambda x: print(x),  #  type: ignore
        )

        return bar