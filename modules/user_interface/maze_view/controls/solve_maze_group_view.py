from modules.maze_solvers.solvers.pledge import PledgeSolver
from modules.maze_solvers.solvers.random_mouse import RandomMouse

# from modules.maze_solvers.solvers.pledge import PledgeSolver
from modules.maze_solvers.solvers.wall_follower import WallFollower
from modules.common_structures.xy import XY
from modules.user_interface.maze_view.controls.solver_controls_dropdown import (
    SolverControlsView,
)
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.maze_view.controls.xy_size_picker import XYPicker
from PyQt6.QtCore import pyqtSignal
from typing import Any, Callable, Optional, Tuple
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SolveMazeGroupView(QWidget):
    setMazeSolverControlsEnabled = pyqtSignal(bool)

    __onSolveButtonPressed: Callable[[MazeSolverSpecification], None]
    __startPosition: XYPicker
    __endPosition: XYPicker
    __mazeSize: XY
    __maximumXY: XY

    def __init__(
        self,
        onPlayButtonPressed: Callable[[], None],
        onPauseButtonPressed: Callable[[], None],
        onStepButtonPressed: Callable[[], None],
        onRestartButtonPressed: Callable[[], None],
        onSpeedControlValueChanged: Callable[[int], None],
        onOpenLogButtonPressed: Callable[[], None],
        onAgentVarsButtonPressed: Callable[[], None],
        onSolveButtonPressed: Callable[[MazeSolverSpecification], None],
        mazeSize: XY,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for controls for solving mazes
        """
        self.__onSolveButtonPressed = onSolveButtonPressed

        self.__mazeSize = mazeSize
        self.__maximumXY = XY(
            self.__mazeSize.x - 1,
            self.__mazeSize.y - 1,
        )

        super().__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        groupbox = QGroupBox("Solve Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        self.__startPosition = XYPicker(
            minimum=XY(0, 0),
            maximum=self.__maximumXY,
            initialValue=XY(0, 0),
            parent=self,
            label="•",
        )

        self.__endPosition = XYPicker(
            minimum=XY(0, 0),
            maximum=self.__maximumXY,
            initialValue=self.__maximumXY,
            parent=self,
            label="•",
        )

        self.__solverTypePicker = QComboBox(self)
        self.__solverTypePicker.addItem("Wall Follower", WallFollower)
        self.__solverTypePicker.addItem("Pledge Solver", PledgeSolver)
        self.__solverTypePicker.addItem("Random Mouse", RandomMouse)

        solveButton = QPushButton("Solve")
        solveButton.clicked.connect(  # type: ignore
            lambda: self.__onSolveButtonPressed(
                MazeSolverSpecification(
                    startPosition=self.__startPosition.getValues(),
                    endPosition=self.__endPosition.getValues(),
                    solverType=self.__solverTypePicker.currentData(),
                ),
            )
        )

        self.__solverControlsDropdown = SolverControlsView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            onSpeedControlValueChanged=onSpeedControlValueChanged,
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            parent=self,
        )
        #  connect enable/disable signal to child view
        self.setMazeSolverControlsEnabled.connect(
            self.__solverControlsDropdown.setMazeSolverControlsEnabled
        )

        vbox.addRow("Start Position", self.__startPosition)
        vbox.addRow("End Position", self.__endPosition)
        vbox.addRow("Solver Type", self.__solverTypePicker)
        vbox.addRow(solveButton)
        vbox.addRow(self.__solverControlsDropdown)

        self.setLayout(layout)
