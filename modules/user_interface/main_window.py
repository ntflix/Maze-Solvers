from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.user_interface.maze_loader_windows.maze_loader_window import (
    MazeLoaderWindow,
)
from typing import List
from PyQt6.QtWidgets import QApplication


class MazeSolverUI(QApplication):
    __maze: MazeProtocol

    def __init__(
        self,
        argv: List[str] = [],
    ) -> None:
        """
        Overarching controller for the whole UI.
        ### Keeps track of:
            • The Maze that has (or has not yet) been generated
        """
        super(MazeSolverUI, self).__init__(argv)

        self.__presentMazeLoader()

    def __presentMazeLoader(self) -> None:
        mazeLoaderWindow = MazeLoaderWindow()
        # connect to method to call when maze is loaded
        mazeLoaderWindow.gotMaze.connect(self.__onMazeLoad)

        mazeLoaderWindow.show()
        self.exec()

    def __onMazeLoad(self, p0: MazeProtocol) -> None:
        self.__maze = p0
        print(self.__maze)


a = MazeSolverUI()
