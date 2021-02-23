from modules.common_structures.xy import XY
from modules.user_interface.maze_view.controls.solve_maze_group_view import (
    SolveMazeGroupView,
)
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Callable, Optional, Tuple
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MazeViewControlsView(QWidget):
    def __init__(
        self,
        onMazeGenerateButtonPressed: Callable[
            [MazeGenerationSpecification],
            None,
        ],
        onMazeSolverSolveButtonPressed: Callable[
            [MazeSolverSpecification],
            None,
        ],
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setMaximumWidth(400)
        self.setContentsMargins(0, 0, 0, 0)

        generateMazeGroupView = GenerateMazeGroupView(parent=self)
        solveMazeGroupView = SolveMazeGroupView(mazeSize=XY(25, 25), parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(generateMazeGroupView)
        layout.addWidget(solveMazeGroupView)

        # add a vertical stretch to the end so all widgets are at the top
        layout.insertStretch(-1)
        self.setLayout(layout)
