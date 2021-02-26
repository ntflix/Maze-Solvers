from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.controls.maze_controls_view import (
    MazeControlsView,
)
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtCore import QSize
from modules.user_interface.maze_view.maze_view import MazeView
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QWidget,
)
from typing import Any, Optional, Tuple


class MazeViewController(QWidget):
    def __init__(
        self,
        maze: MazeProtocol,
        parent: Optional[QWidget] = None,
        minimumMazeSize: QSize = QSize(400, 400),
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The view controller for the MazeView and its controls bar.
        """
        super(MazeViewController, self).__init__(parent=parent, *args, **kwargs)

        self.__maze = maze

        layout = QHBoxLayout()

        layout.addWidget(
            MazeView(
                minimumSize=minimumMazeSize,
                maze=self.__maze,
                parent=self,
                keepAspectRatio=False,
            )
        )

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        layout.addWidget(
            MazeControlsView(
                onPlayButtonPressed=self.__onPlayButtonPressed,
                onPauseButtonPressed=self.__onPauseButtonPressed,
                onStepButtonPressed=self.__onStepButtonPressed,
                onRestartButtonPressed=self.__onRestartButtonPressed,
                onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
                onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
                onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
                onGenerateMazeButtonPressed=self.__onMazeGenerateButtonPressed,
            )
        )

        self.setLayout(layout)
        # self.show()

    def __onMazeGenerateButtonPressed(self, p0: MazeGenerationSpecification) -> None:
        print(p0)

    def __onPlayButtonPressed(self) -> None:
        print("thing")

    def __onPauseButtonPressed(self) -> None:
        print("thing")

    def __onStepButtonPressed(self) -> None:
        print("thing")

    def __onRestartButtonPressed(self) -> None:
        print("thing")

    def __onSpeedControlValueChanged(self) -> None:
        print("thing")

    def __onOpenLogButtonPressed(self) -> None:
        print("thing")

    def __onAgentVarsButtonPressed(self) -> None:
        print("thing")
