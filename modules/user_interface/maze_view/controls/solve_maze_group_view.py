from modules.common_structures.xy import XY
from modules.user_interface.maze_view.controls.solver_controls_dropdown import (
    SolverControlsView,
)
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.maze_view.controls.xy_size_picker import XYPicker
from PyQt6.QtCore import pyqtSignal, PYQT_SLOT
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SolveMazeGroupView(QWidget):
    onSolveButtonPressed = pyqtSignal(MazeSolverSpecification)
    __startPosition: XYPicker
    __endPosition: XYPicker
    __mazeSize: XY
    __maximumXY: XY

    def __init__(
        self,
        onPlayButtonPressed: PYQT_SLOT,
        onPauseButtonPressed: PYQT_SLOT,
        onStepButtonPressed: PYQT_SLOT,
        onRestartButtonPressed: PYQT_SLOT,
        onSpeedControlValueChanged: PYQT_SLOT,
        onOpenLogButtonPressed: PYQT_SLOT,
        onAgentVarsButtonPressed: PYQT_SLOT,
        mazeSize: XY,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for controls for solving mazes
        """
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
            initialValue=XY(0, 0),
            parent=self,
            label="•",
        )

        solveButton = QPushButton("Solve")
        solveButton.clicked.connect(  # type: ignore
            lambda: self.__onSolveButtonPressed(
                p0=MazeSolverSpecification(
                    startPosition=self.__startPosition.getValues(),
                    endPosition=self.__endPosition.getValues(),
                ),
            )
        )

        solverControlsDropdown = SolverControlsView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            onSpeedControlValueChanged=onSpeedControlValueChanged,
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            parent=self,
        )

        vbox.addRow("Start Position", self.__startPosition)
        vbox.addRow("End Position", self.__endPosition)
        vbox.addRow(solveButton)
        vbox.addRow(solverControlsDropdown)

        self.setLayout(layout)

    def __onSolveButtonPressed(self, p0: MazeSolverSpecification) -> None:
        print("solve button pressed")
        self.onSolveButtonPressed.emit(p0)
