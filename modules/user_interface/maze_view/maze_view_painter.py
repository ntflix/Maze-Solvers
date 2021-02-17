from typing import Any, Optional, Tuple
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtGui import QPainter, QPainterPath, QPaintEvent, QResizeEvent
from PyQt6.QtCore import QPointF, QSize
from PyQt6.QtWidgets import QWidget


class MazeViewPainter(QWidget):
    __painter: QPainter
    __maze: MazeProtocol

    def __init__(
        self,
        size: QSize,
        maze: MazeProtocol,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ):
        super().__init__(parent)

        self.__maze = maze

        self.setMinimumSize(size)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        # Force the widget to rezise with a 1:1 aspect ratio
        smallestAxisSize = min(a0.size().width(), a0.size().height())
        newSize = QSize(smallestAxisSize, smallestAxisSize)
        self.resize(newSize)
        return super().resizeEvent(a0)

    def paintEvent(self, a0: QPaintEvent) -> None:
        # Initialise a painter to paint on this widget
        self.__painter = QPainter(self)

        mazePath = self.__createMazePath()
        self.__painter.drawPath(mazePath)

        self.__painter.drawRect(
            0,  # x
            0,  # y
            self.width() - 1,  # width
            self.height() - 1,  # height
        )

        self.__painter.drawText(
            QPointF(50, 50),
            "MazeView Not Implemented",
        )

        print(self.__maze)

        self.__painter.end()

    def __createMazePath(self) -> QPainterPath:
        path = QPainterPath(QPointF(0, 0))

        return path