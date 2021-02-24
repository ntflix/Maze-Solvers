from PyQt6.QtCore import PYQT_SLOT
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
        onPlayButtonPressed: PYQT_SLOT,
        onPauseButtonPressed: PYQT_SLOT,
        onStepButtonPressed: PYQT_SLOT,
        onRestartButtonPressed: PYQT_SLOT,
        onSpeedControlValueChanged: PYQT_SLOT,
        onOpenLogButtonPressed: PYQT_SLOT,
        onAgentVarsButtonPressed: PYQT_SLOT,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setMaximumWidth(400)
        self.setContentsMargins(0, 0, 0, 0)

        generateMazeGroupView = GenerateMazeGroupView(parent=self)
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
