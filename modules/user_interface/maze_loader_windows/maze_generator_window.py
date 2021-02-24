from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtCore import pyqtSignal
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QMainWindow, QWidget


class MazeGeneratorWindow(QMainWindow):
    onMazeSpecChosen = pyqtSignal(MazeGenerationSpecification)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A window presented to the user prompting them for maze specification.
        """
        super(MazeGeneratorWindow, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(15, 5, 15, 15)

        generateMazeView = GenerateMazeGroupView(parent=self)
        generateMazeView.onMazeSpecChosen.connect(self.onMazeSpecChosen)

        self.setCentralWidget(generateMazeView)

        self.setWindowTitle("Generate a Maze")

        self.show()
