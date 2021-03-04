from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from PyQt6.QtCore import pyqtSignal
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_loader_windows.maze_loader_view import MazeLoaderView
from modules.user_interface.maze_view.maze_view_window import MazeViewWindow
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Callable, List
from PyQt6.QtWidgets import QApplication


class MazeSolverUI(QApplication):
    __mazeLoaderWindow: MazeLoaderView
    __mazeViewWindow: MazeViewWindow

    __onLoadLastMazePressed: Callable[[], None]
    __onMazeFilePathChosen: Callable[[str], None]
    __onPlayButtonPressed: Callable[[], None]
    __onPauseButtonPressed: Callable[[], None]
    __onStepButtonPressed: Callable[[], None]
    __onRestartButtonPressed: Callable[[], None]
    __onSpeedControlValueChanged: Callable[[int], None]
    __onOpenLogButtonPressed: Callable[[], None]
    __onAgentVarsButtonPressed: Callable[[], None]
    __onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None]
    __onSolveButtonPressed: Callable[[MazeSolverSpecification], None]

    setMazeSolverControlsEnabled = pyqtSignal(bool)
    setMazeGeneratorControlsEnabled = pyqtSignal(bool)

    def __init__(
        self,
        onLoadLastMazePressed: Callable[[], None],
        onMazeFilePathChosen: Callable[[str], None],
        onPlayButtonPressed: Callable[[], None],
        onPauseButtonPressed: Callable[[], None],
        onStepButtonPressed: Callable[[], None],
        onRestartButtonPressed: Callable[[], None],
        onSpeedControlValueChanged: Callable[[int], None],
        onOpenLogButtonPressed: Callable[[], None],
        onAgentVarsButtonPressed: Callable[[], None],
        onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None],
        onSolveButtonPressed: Callable[[MazeSolverSpecification], None],
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
        self.__onSolveButtonPressed = onSolveButtonPressed

    def showMazeLoader(self) -> None:
        # construct a maze loader view
        self.__mazeLoaderWindow = MazeLoaderView(
            onMazeLoadedFromPath=self.__onMazeFilePathChosen,
            onLoadLastMazePressed=self.__onLoadLastMazePressed,
            onMazeSpecificationChosen=self.__onGenerateMazeButtonPressed,
        )
        # connect to method to call when maze is loaded
        self.__mazeLoaderWindow.show()

    def showMazeViewWindow(self, maze: MazeProtocol) -> None:
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
                onSolveButtonPressed=self.__onSolveButtonPressed,
            )
        except:
            raise UnboundLocalError(
                "Attempted to load a maze that had not yet been instantiated."
            )

        # connect enable/disable view signals
        self.setMazeSolverControlsEnabled.connect(
            self.__mazeViewWindow.setMazeSolverControlsEnabled
        )
        self.setMazeGeneratorControlsEnabled.connect(
            self.__mazeViewWindow.setMazeGeneratorControlsEnabled
        )

        self.__mazeViewWindow.show()
