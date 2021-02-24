from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtCore import pyqtSlot
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
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setMaximumWidth(400)
        self.setContentsMargins(0, 0, 0, 0)

        generateMazeGroupView = GenerateMazeGroupView(
            onGenerateButtonPressed=onGenerateMazeButtonPressed,
            parent=self,
        )

        solveMazeGroupView = SolveMazeGroupView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            onSpeedControlValueChanged=onSpeedControlValueChanged,
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            mazeSize=XY(25, 25),
            parent=self,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(generateMazeGroupView)
        layout.addWidget(solveMazeGroupView)

        # add a vertical stretch to the end so all widgets are at the top
        layout.insertStretch(-1)
        self.setLayout(layout)
