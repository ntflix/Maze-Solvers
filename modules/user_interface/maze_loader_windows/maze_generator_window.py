from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtCore import pyqtSlot
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QMainWindow, QWidget


class MazeGeneratorWindow(QMainWindow):
    def __init__(
        self,
        onMazeGenerateButtonPressedWithSpecification: pyqtSlot(
            MazeGenerationSpecification
        ),
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A window presented to the user prompting them for maze specification.
        """
        super(MazeGeneratorWindow, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(15, 5, 15, 15)

        generateMazeView = GenerateMazeGroupView(
            onGenerateButtonPressed=onMazeGenerateButtonPressedWithSpecification,
            parent=self,
        )

        self.setCentralWidget(generateMazeView)

        self.setWindowTitle("Generate a Maze")

        self.show()
