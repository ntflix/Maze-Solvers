from modules.user_interface.ui_translation_data_structures.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation_data_structures.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Callable, Optional, Tuple
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MazeViewControlsView(QWidget):
    __mazeSolverOptionsEnabled: bool

    def __init__(
        self,
        # `Awaitable`s mean that a callable function is asynchronous.
        # Async functions, in this context, free up the UI to respond to events and do not block the main thread.
        onMazeGenerateButtonPressed: Callable[
            [MazeGenerationSpecification],
            None,
        ],
        onMazeSolverSolveButtonPressed: Callable[
            [MazeSolverSpecification],
            None,
        ],
        mazeSolverOptionsEnabled: bool = False,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        super().__init__(parent=parent, *args, **kwargs)

        self.__mazeSolverOptionsEnabled = mazeSolverOptionsEnabled

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            GenerateMazeGroupView(
                onMazeGenerateButtonPressed,
                parent=self,
            )
        )

    def setMazeSolverOptionsEnabled(self, enabled: bool) -> None:
        if self.__mazeSolverOptionsEnabled != enabled:
            self.__mazeSolverOptionsEnabled = enabled
        else:
            raise ValueError("Maze Solver Options are already enabled")
