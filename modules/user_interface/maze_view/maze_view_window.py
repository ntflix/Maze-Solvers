from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal
from modules.user_interface.maze_view.maze_view_controller import MazeViewController
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Any, Callable, Optional, Tuple
from PyQt6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QWidget,
)


class MazeViewWindow(QMainWindow):
    __onPlayButtonPressed: Callable[[], None]
    __onPauseButtonPressed: Callable[[], None]
    __onStepButtonPressed: Callable[[], None]
    __onRestartButtonPressed: Callable[[], None]
    __onSpeedControlValueChanged: Callable[[int], None]
    __onOpenLogButtonPressed: Callable[[], None]
    __onAgentVarsButtonPressed: Callable[[], None]
    __onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None]
    __onSolveButtonPressed: Callable[[MazeSolverSpecification], None]

    onMazeSolverAgentUpdate = pyqtSignal(MazeSolver)
    setMazeSolverControlsEnabled = pyqtSignal(bool)
    setMazeGeneratorControlsEnabled = pyqtSignal(bool)

    def __init__(
        self,
        maze: MazeProtocol,
        solver: Optional[MazeSolver],
        onPlayButtonPressed: Callable[[], None],
        onPauseButtonPressed: Callable[[], None],
        onStepButtonPressed: Callable[[], None],
        onRestartButtonPressed: Callable[[], None],
        onSpeedControlValueChanged: Callable[[int], None],
        onOpenLogButtonPressed: Callable[[], None],
        onAgentVarsButtonPressed: Callable[[], None],
        onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None],
        onSolveButtonPressed: Callable[[MazeSolverSpecification], None],
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A MazeView with controls.
        """
        super(MazeViewWindow, self).__init__(parent)

        self.__onPlayButtonPressed = onPlayButtonPressed
        self.__onPauseButtonPressed = onPauseButtonPressed
        self.__onStepButtonPressed = onStepButtonPressed
        self.__onRestartButtonPressed = onRestartButtonPressed
        self.__onSpeedControlValueChanged = onSpeedControlValueChanged
        self.__onOpenLogButtonPressed = onOpenLogButtonPressed
        self.__onGenerateMazeButtonPressed = onGenerateMazeButtonPressed
        self.__onAgentVarsButtonPressed = onAgentVarsButtonPressed
        self.__onSolveButtonPressed = onSolveButtonPressed

        mazeViewController = MazeViewController(
            maze=maze,
            solver=solver,
            onPlayButtonPressed=self.__onPlayButtonPressed,
            onPauseButtonPressed=self.__onPauseButtonPressed,
            onStepButtonPressed=self.__onStepButtonPressed,
            onRestartButtonPressed=self.__onRestartButtonPressed,
            onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
            onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
            onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
            onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            onSolveButtonPressed=self.__onSolveButtonPressed,
            parent=self,
            *args,
            **kwargs,
        )

        # connect the onMazeSolverAgentUpdate signal to the mazeViewController
        self.onMazeSolverAgentUpdate.connect(
            mazeViewController.onMazeSolverAgentUpdate,
        )

        # connect enable/disable view signal for maze generator controls enabled
        self.setMazeGeneratorControlsEnabled.connect(
            mazeViewController.setMazeGeneratorControlsEnabled,
        )

        # connect enable/disable view signal for maze solver controls enabled
        self.setMazeSolverControlsEnabled.connect(
            mazeViewController.setMazeSolverControlsEnabled,
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