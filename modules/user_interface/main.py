from modules.user_interface.ui_translation_data_structures.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation_data_structures.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.maze_view_controller import MazeViewController
from modules.user_interface.maze_view.controls.maze_view_controls_view import (
    MazeViewControlsView,
)
from modules.data_structures.maze.maze import Maze
from typing import List
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLayout,
    QWidget,
)


class MazeSolverUIApplication:
    __application: QApplication
    __window: QWidget

    def __init__(
        self,
        argv: List[str] = [],
    ) -> None:
        self.__application = QApplication(argv)

    def exec(self) -> int:
        self.__window = QWidget()
        self.__window.setWindowTitle("Maze Solvers")

        self.__window.setLayout(self.__getLayout())
        self.__window.show()

        return self.__application.exec()

    def __getLayout(self) -> QLayout:
        layout = QHBoxLayout()

        # layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            MazeViewController(
                minimumSize=QSize(400, 400),
                maze=Maze(40, 30),
                parent=self.__window,
            )
        )

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        layout.addWidget(
            MazeViewControlsView(
                onMazeGenerateButtonPressed=self.__onMazeGenerateButtonPressed,
                onMazeSolverSolveButtonPressed=self.__onMazeSolverSolveButtonPressed,
            )
        )

        return layout

    def __onMazeGenerateButtonPressed(
        self, mazeSpec: MazeGenerationSpecification
    ) -> None:
        return None

    def __onMazeSolverSolveButtonPressed(
        self, mazeSolverSpec: MazeSolverSpecification
    ) -> None:
        print("Pressed Solve")
        return None


main = MazeSolverUIApplication()
main.exec()
