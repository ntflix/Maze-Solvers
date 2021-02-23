from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.maze_view.controls.xy_size_picker import XYPicker
from PyQt6 import QtCore
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SolveMazeGroupView(QWidget):
    onSolveButtonPressed = QtCore.pyqtSignal(MazeSolverSpecification)
    __startPosition: XYPicker
    __endPosition: XYPicker

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for controls for solving mazes
        """
        super().__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        groupbox = QGroupBox("Solve Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        self.__startPosition = XYPicker(self)
        self.__endPosition = XYPicker(self)

        solveButton = QPushButton("Generate")
        solveButton.clicked.connect(  # type: ignore
            lambda: self.__onSolveButtonPressed(
                p0=MazeSolverSpecification(
                    startPosition=self.__startPosition.getValues(),
                    endPosition=self.__endPosition.getValues(),
                ),
            )
        )

        vbox.addRow("Start Position", self.__startPosition)
        vbox.addRow("End Position", self.__endPosition)
        vbox.addRow(solveButton)

        self.setLayout(layout)

    def __onSolveButtonPressed(self, p0: MazeSolverSpecification) -> None:
        print("generate button pressed")
        self.onSolveButtonPressed.emit(p0)
