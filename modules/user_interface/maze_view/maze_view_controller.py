from PyQt6.QtCore import QSize
from modules.user_interface.maze_view.maze_view import MazeView
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QGridLayout, QWidget
from PyQt6.QtGui import QMouseEvent


class MazeViewController(QWidget):
    __maze: MazeProtocol

    def __init__(
        self,
        minimumSize: QSize,
        maze: MazeProtocol,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Controller for the main MazeView. Handles click events.
        """
        super().__init__(parent=parent, *args, **kwargs)

        self.__maze = maze
        self.__drawAsIs(minimumSize, *args, **kwargs)

    def __drawAsIs(
        self,
        minimumSize: QSize,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ):
        layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            MazeView(
                minimumSize=minimumSize,
                maze=self.__maze,
                parent=self,
                keepAspectRatio=False,
                *args,
                **kwargs,
            ),
        )

        self.setLayout(layout)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        # Resizing does not work correctly on the pop-out window, hence this being disabled.
        print(
            (
                "mouseDoubleClickEvent on MazeViewController. "
                "If you would like to enable a separate window for showing the maze, "
                "please uncomment the relevant lines in the `mouseDoubleClickEvent` function "
                "in `modules/user_interface/maze_view/maze_view_controller.py`."
            )
        )
        # dialog = MazeViewWindow(self, maze=self.__maze)
        # dialog.show()
        return super().mouseDoubleClickEvent(a0)