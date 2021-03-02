from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_loader_windows.maze_loader_view import MazeLoaderView
from modules.user_interface.maze_view.maze_view_window import MazeViewWindow
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import List, Optional
from PyQt6.QtWidgets import QApplication


class MazeSolverUI(QApplication):
    __maze: Optional[MazeProtocol]
    __mazeLoaderWindow: MazeLoaderView
    __mazeViewWindow: MazeViewWindow

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

        self.__showMazeLoader()

    def __showMazeLoader(self) -> None:
        # construct a maze loader view
        self.__mazeLoaderWindow = MazeLoaderView(
            onMazeLoaded=self.__onMazeLoad,
            onLoadLastMazePressed=self.__onLoadLastMazeChosen,
            onMazeSpecificationChosen=self.__onMazeSpecificationChosen,
        )
        # connect to method to call when maze is loaded
        self.__mazeLoaderWindow.show()

    def __onMazeSpecificationChosen(self, p0: MazeGenerationSpecification) -> None:
        # self.__maze = Maze(p0.size.x, p0.size.y)
        self.__showMazeViewWindow()

    def __onLoadLastMazeChosen(self) -> None:
        print("load last selected")

    def __showMazeViewWindow(self) -> None:
        self.__mazeLoaderWindow.destroy(True, True)

        try:
            self.__mazeViewWindow = MazeViewWindow(maze=self.__maze)
        except:
            raise UnboundLocalError(
                "Attempted to load a maze that had not yet been instantiated."
            )

        self.__mazeViewWindow.show()

    def __onMazeLoad(self, p0: MazeProtocol) -> None:
        self.__maze = p0

        # destroy the maze loader view
        self.__mazeLoaderWindow.destroy(  # type: ignore # override optional
            True,  # destroy window
            True,  # destroy sub-windows
        )

        self.__showMazeViewWindow()


if __name__ == "__main__":
    import logging

    FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
    LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LEVEL)
    log = logging.getLogger()

    a = MazeSolverUI()
    a.exec()