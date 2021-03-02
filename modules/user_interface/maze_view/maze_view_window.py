from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import pyqtSlot
from modules.user_interface.maze_view.maze_view_controller import MazeViewController
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QWidget,
)


class MazeViewWindow(QMainWindow):
    __onPlayButtonPressed: pyqtSlot()
    __onPauseButtonPressed: pyqtSlot()
    __onStepButtonPressed: pyqtSlot()
    __onRestartButtonPressed: pyqtSlot()
    __onSpeedControlValueChanged: pyqtSlot(int)
    __onOpenLogButtonPressed: pyqtSlot()
    __onAgentVarsButtonPressed: pyqtSlot()
    __onGenerateMazeButtonPressed: pyqtSlot(MazeGenerationSpecification)
    __onSolveButtonPressed: pyqtSlot(MazeSolverSpecification)

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
        onSolveButtonPressed: pyqtSlot(MazeSolverSpecification),
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A MazeView with controls.
        """
        super(MazeViewWindow, self).__init__(parent)

        self.__onPlayButtonPressed = onPlayButtonPressed
        self.__onPauseButtonPressed = onPauseButtonPressed
        self.__onStepButtonPressed = onStepButtonPressed
        self.__onRestartButtonPressed = onRestartButtonPressed
        self.__onSpeedControlValueChanged = onSpeedControlValueChanged
        self.__onOpenLogButtonPressed = onOpenLogButtonPressed
        self.__onGenerateMazeButtonPressed = onGenerateMazeButtonPressed
        self.__onAgentVarsButtonPressed = onAgentVarsButtonPressed
        self.__onSolveButtonPressed = onSolveButtonPressed

        mazeViewController = MazeViewController(
            maze=maze,
            onPlayButtonPressed=self.__onPlayButtonPressed,
            onPauseButtonPressed=self.__onPauseButtonPressed,
            onStepButtonPressed=self.__onStepButtonPressed,
            onRestartButtonPressed=self.__onRestartButtonPressed,
            onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
            onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
            onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
            onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            onSolveButtonPressed=self.__onSolveButtonPressed,
            parent=self,
            *args,
            **kwargs,
        )

        self.setMenuBar(self.__getMenuBar())
        self.setCentralWidget(mazeViewController)

    def __getMenuBar(self) -> QMenuBar:
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.addAction("New")

        save = QAction("Save", self)
        save.setShortcut(QKeySequence.StandardKey.Save)
        file.addAction(save)

        edit = bar.addMenu("Edit")
        edit.addAction("copy")
        edit.addAction("paste")

        quit = QAction("Quit", self)
        file.addAction(quit)

        file.triggered.connect(  # type: ignore
            lambda x: print(x),  #  type: ignore
        )

        return bar