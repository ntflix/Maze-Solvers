from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_view.controls.maze_controls_view import (
    MazeControlsView,
)
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtCore import QSize, pyqtSlot
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
        onPlayButtonPressed: pyqtSlot(),
        onPauseButtonPressed: pyqtSlot(),
        onStepButtonPressed: pyqtSlot(),
        onRestartButtonPressed: pyqtSlot(),
        onSpeedControlValueChanged: pyqtSlot(int),
        onOpenLogButtonPressed: pyqtSlot(),
        onAgentVarsButtonPressed: pyqtSlot(),
        onGenerateMazeButtonPressed: pyqtSlot(MazeGenerationSpecification),
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
                onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            )
        )

        self.setLayout(layout)

    def __onGenerateMazeButtonPressed(self, p0: MazeGenerationSpecification) -> None:
        print(p0)

    def __onPlayButtonPressed(self) -> None:
        print("__onPlayButtonPressed")

    def __onPauseButtonPressed(self) -> None:
        print("__onPauseButtonPressed")

    def __onStepButtonPressed(self) -> None:
        print("__onStepButtonPressed")

    def __onRestartButtonPressed(self) -> None:
        print("__onRestartButtonPressed")

    def __onSpeedControlValueChanged(self) -> None:
        print("__onSpeedControlValueChanged")

    def __onOpenLogButtonPressed(self) -> None:
        print("__onOpenLogButtonPressed")

    def __onAgentVarsButtonPressed(self) -> None:
        print("__onAgentVarsButtonPressed")
