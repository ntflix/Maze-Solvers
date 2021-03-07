from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver
from modules.maze_solvers.maze_solver_state import MazeSolverState
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.controls.maze_controls_view import (
    MazeControlsView,
)
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtCore import QSize, pyqtSignal
from modules.user_interface.maze_view.maze_view import MazeView
from typing import Any, Callable, Optional, Tuple
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QWidget,
)
from typing import Any, Optional, Tuple


class MazeViewController(QWidget):

    setMazeSolverControlsEnabled = pyqtSignal(bool)
    setMazeGeneratorControlsEnabled = pyqtSignal(bool)
    onMazeSolverAgentUpdate = pyqtSignal(MazeSolver)

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
        onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None],
        onSolveButtonPressed: Callable[[MazeSolverSpecification], None],
        onAgentVariablesButtonPressed: Callable[[], None],
        parent: Optional[QWidget] = None,
        minimumMazeSize: QSize = QSize(400, 400),
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The view controller for the MazeView and its controls bar.
        """
        super(MazeViewController, self).__init__(parent=parent, *args, **kwargs)

        self.__onPlayButtonPressed = onPlayButtonPressed
        self.__onPauseButtonPressed = onPauseButtonPressed
        self.__onStepButtonPressed = onStepButtonPressed
        self.__onRestartButtonPressed = onRestartButtonPressed
        self.__onSpeedControlValueChanged = onSpeedControlValueChanged
        self.__onOpenLogButtonPressed = onOpenLogButtonPressed
        self.__onGenerateMazeButtonPressed = onGenerateMazeButtonPressed
        self.__onSolveButtonPressed = onSolveButtonPressed
        self.__onAgentVarsButtonPressed = onAgentVariablesButtonPressed

        self.__maze = maze

        layout = QHBoxLayout()

        # safely unwrap optional solver state
        # init solverState as None so it is not unbound
        solverState: Optional[MazeSolverState] = None
        if solver is not None:
            # solver has been passed to class
            # check it is of type MazeSolverState (mainly for static type analysis)
            if type(solver) == MazeSolverState:
                # set solverState to the current state of our solver
                solverState = solver.getCurrentState()

        self.__mazeView = MazeView(
            minimumSize=minimumMazeSize,
            maze=self.__maze,
            solverState=solverState,
            parent=self,
            keepAspectRatio=False,
        )

        # connect private method to the onSolverAgentUpdate signal
        self.onMazeSolverAgentUpdate.connect(self.__onMazeSolverAgentUpdate)

        layout.addWidget(self.__mazeView)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        self.__mazeControlsView = MazeControlsView(
            onPlayButtonPressed=self.__onPlayButtonPressed,
            onPauseButtonPressed=self.__onPauseButtonPressed,
            onStepButtonPressed=self.__onStepButtonPressed,
            onRestartButtonPressed=self.__onRestartButtonPressed,
            onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
            onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
            onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
            onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            onSolveButtonPressed=self.__onSolveButtonPressed,
            mazeSize=self.__maze.size,
        )

        layout.addWidget(self.__mazeControlsView)

        self.setLayout(layout)

        # connect the signals
        self.setMazeGeneratorControlsEnabled.connect(
            self.__mazeControlsView.setMazeGeneratorControlsEnabled
        )
        self.setMazeSolverControlsEnabled.connect(
            self.__mazeControlsView.setMazeSolverControlsEnabled
        )

    def __onMazeSolverAgentUpdate(self, solver: MazeSolver) -> None:
        # define a method to connect solver state updates with the MazeView
        self.__mazeView.onMazeSolverAgentUpdate.emit(
            # send the current state to the mazeview so it can draw new state
            solver.getCurrentState()
        )
