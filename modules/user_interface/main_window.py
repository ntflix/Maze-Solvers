from PyQt6.QtCore import pyqtSlot
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_loader_windows.maze_loader_view import MazeLoaderView
from modules.user_interface.maze_view.maze_view_window import MazeViewWindow
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import List
from PyQt6.QtWidgets import QApplication


class MazeSolverUI(QApplication):
    __mazeLoaderWindow: MazeLoaderView
    __mazeViewWindow: MazeViewWindow

    __onLoadLastMazePressed: pyqtSlot()
    __onMazeFilePathChosen: pyqtSlot(str)
    __onPlayButtonPressed: pyqtSlot()
    __onPauseButtonPressed: pyqtSlot()
    __onStepButtonPressed: pyqtSlot()
    __onRestartButtonPressed: pyqtSlot()
    __onSpeedControlValueChanged: pyqtSlot(int)
    __onOpenLogButtonPressed: pyqtSlot()
    __onAgentVarsButtonPressed: pyqtSlot()
    __onGenerateMazeButtonPressed: pyqtSlot(MazeGenerationSpecification)

    def __init__(
        self,
        onLoadLastMazePressed: pyqtSlot(),
        onMazeFilePathChosen: pyqtSlot(str),
        onPlayButtonPressed: pyqtSlot(),
        onPauseButtonPressed: pyqtSlot(),
        onStepButtonPressed: pyqtSlot(),
        onRestartButtonPressed: pyqtSlot(),
        onSpeedControlValueChanged: pyqtSlot(int),
        onOpenLogButtonPressed: pyqtSlot(),
        onAgentVarsButtonPressed: pyqtSlot(),
        onGenerateMazeButtonPressed: pyqtSlot(MazeGenerationSpecification),
        argv: List[str] = [],
    ) -> None:
        """
        Overarching controller for the whole UI.
        ### Keeps track of:
            • The Maze that has (or has not yet) been generated
        """
        super(MazeSolverUI, self).__init__(argv)

        self.__onLoadLastMazePressed = onLoadLastMazePressed
        self.__onMazeFilePathChosen = onMazeFilePathChosen
        self.__onPlayButtonPressed = onPlayButtonPressed
        self.__onPauseButtonPressed = onPauseButtonPressed
        self.__onStepButtonPressed = onStepButtonPressed
        self.__onRestartButtonPressed = onRestartButtonPressed
        self.__onSpeedControlValueChanged = onSpeedControlValueChanged
        self.__onOpenLogButtonPressed = onOpenLogButtonPressed
        self.__onAgentVarsButtonPressed = onAgentVarsButtonPressed
        self.__onGenerateMazeButtonPressed = onGenerateMazeButtonPressed

        self.__showMazeLoader()

    def __showMazeLoader(self) -> None:
        # construct a maze loader view
        self.__mazeLoaderWindow = MazeLoaderView(
            onMazeFilePathChosen=self.__onMazeFilePathChosen,
            onLoadLastMazePressed=self.__onLoadLastMazePressed,
            onMazeSpecificationChosen=self.__onGenerateMazeButtonPressed,
        )
        # connect to method to call when maze is loaded
        self.__mazeLoaderWindow.show()

    def __showMazeViewWindow(self, maze: MazeProtocol) -> None:
        self.__mazeLoaderWindow.destroy(True, True)

        try:
            self.__mazeViewWindow = MazeViewWindow(
                maze=maze,
                onPlayButtonPressed=self.__onPlayButtonPressed,
                onPauseButtonPressed=self.__onPauseButtonPressed,
                onStepButtonPressed=self.__onStepButtonPressed,
                onRestartButtonPressed=self.__onRestartButtonPressed,
                onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
                onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
                onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
                onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            )
        except:
            raise UnboundLocalError(
                "Attempted to load a maze that had not yet been instantiated."
            )

        self.__mazeViewWindow.show()

    # def __onMazeLoad(self, p0: MazeProtocol) -> None:

    #     # destroy the maze loader view
    #     self.__mazeLoaderWindow.destroy(  # type: ignore # override optional
    #         True,  # destroy window
    #         True,  # destroy sub-windows
    #     )

    #     self.__showMazeViewWindow(p0)
