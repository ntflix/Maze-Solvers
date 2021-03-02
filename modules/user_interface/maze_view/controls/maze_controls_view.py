from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from modules.common_structures.xy import XY
from modules.user_interface.maze_view.controls.solve_maze_group_view import (
    SolveMazeGroupView,
)
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MazeControlsView(QWidget):
    setMazeSolverControlsEnabled = pyqtSignal(bool)
    setMazeGeneratorControlsEnabled = pyqtSignal(bool)

    def __init__(
        self,
        onPlayButtonPressed: pyqtSlot(),
        onPauseButtonPressed: pyqtSlot(),
        onStepButtonPressed: pyqtSlot(),
        onRestartButtonPressed: pyqtSlot(),
        onSpeedControlValueChanged: pyqtSlot(int),
        onOpenLogButtonPressed: pyqtSlot(),
        onAgentVarsButtonPressed: pyqtSlot(),
        onGenerateMazeButtonPressed: pyqtSlot(MazeGenerationSpecification),
        onSolveButtonPressed: pyqtSlot(MazeSolverSpecification),
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """A vertical view of maze generator and solver agent controls views.

        Parameters
        ----------
        onPlayButtonPressed : pyqtSlot()
        onPauseButtonPressed : pyqtSlot()
        onStepButtonPressed : pyqtSlot()
        onRestartButtonPressed : pyqtSlot()
        onSpeedControlValueChanged : pyqtSlot()
        onOpenLogButtonPressed : pyqtSlot()
        onAgentVarsButtonPressed : pyqtSlot()
        onGenerateMazeButtonPressed : pyqtSlot(MazeGenerationSpecification)
        onSolveButtonPressed: pyqtSlot(MazeSolverSpecification)
        parent : Optional[QWidget], optional
            Parent widget, by default None
        """
        super().__init__(parent=parent, *args, **kwargs)
        self.setMaximumWidth(400)
        self.setContentsMargins(0, 0, 0, 0)

        generateMazeGroupView = GenerateMazeGroupView(parent=self)
        generateMazeGroupView.onMazeSpecChosen.connect(onGenerateMazeButtonPressed)
        # connect the enable/disable generateMazeGroupView signal to a lambda that enables/disables the generateMazeGroupView
        self.setMazeGeneratorControlsEnabled.connect(generateMazeGroupView.setEnabled)

        solveMazeGroupView = SolveMazeGroupView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            onSpeedControlValueChanged=onSpeedControlValueChanged,
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            onSolveButtonPressed=onSolveButtonPressed,
            mazeSize=XY(25, 25),
            parent=self,
        )
        # connect the enable/disable solver controls signal to a lambda that enables/disables the solver controls
        self.setMazeSolverControlsEnabled.connect(
            solveMazeGroupView.setMazeSolverControlsEnabled
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(generateMazeGroupView)
        layout.addWidget(solveMazeGroupView)

        # add a vertical stretch to the end so all widgets are at the top
        layout.insertStretch(-1)
        self.setLayout(layout)
