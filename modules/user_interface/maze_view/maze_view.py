from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.common_structures.xy import XY
from typing import Any, Optional, Set, Tuple
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtGui import (
    QPainter,
    QPainterPath,
    QPaintEvent,
    QResizeEvent,
)
from PyQt6.QtCore import QPointF, QSize
from PyQt6.QtWidgets import QWidget


class MazeView(QWidget):
    __painter: QPainter
    __maze: MazeProtocol
    __keepAspectRatio: bool

    def __init__(
        self,
        minimumSize: QSize,
        maze: MazeProtocol,
        parent: Optional[QWidget] = None,
        keepAspectRatio: bool = True,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ):
        super().__init__(parent=parent, *args, **kwargs)

        self.__keepAspectRatio = keepAspectRatio
        self.__maze = maze

        self.setContentsMargins(0, 0, 0, 0)

        self.setMinimumSize(minimumSize)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.__keepAspectRatio:
            # Force the widget to rezise with a 1:1 aspect ratio
            # first calculate the smallest size axis:
            smallestAxisSize = min(a0.size().width(), a0.size().height())
            # set a newSize var with this as both the axes sizes
            newSize = QSize(smallestAxisSize, smallestAxisSize)
            # resize with this new 1:1 size
            self.resize(newSize)
            # force resizeEvent of super with implicitly modified resize

        return super().resizeEvent(a0)

    def paintEvent(self, a0: QPaintEvent) -> None:
        # Initialise a painter to paint on this widget
        self.__painter = QPainter(self)

        mazePath = self.__createMazePath()
        self.__painter.drawPath(mazePath)

        self.__painter.end()

    def __createMazePath(self) -> QPainterPath:
        cellSize = (
            self.width() / self.__maze.size.x,
            self.height() / self.__maze.size.y,
        )

        path = QPainterPath(QPointF(0, 0))

        # draw outline of maze
        path.addRect(
            0,
            0,
            self.width() - 1,
            self.height() - 1,
        )

        for y in range(self.__maze.size.y):
            currentY = y * cellSize[1]

            for x in range(self.__maze.size.y):
                currentX = x * cellSize[0]

                # get the list of walls surrounding this cell
                thisCellsWalls: Set[
                    AbsoluteDirection
                ] = self.__maze.getWallsOfCellAtCoordinate(XY(x, y))

                # draw north and west walls only, because the next iterations will draw the south and east walls for us (don't wanna waste paint /s)
                if AbsoluteDirection.west in thisCellsWalls:
                    path.moveTo(currentX, currentY)
                    path.lineTo(currentX, currentY + cellSize[1])

                if AbsoluteDirection.north in thisCellsWalls:
                    path.moveTo(currentX, currentY)
                    path.lineTo(currentX + cellSize[0], currentY)

        return path

    # def __createMazePath(
    #     self,
    # ) -> QPainterPath:
    #     cellSize = (
    #         self.width() / self.__maze.size.x,
    #         self.height() / self.__maze.size.y,
    #     )

    #     path = QPainterPath(QPointF(0, 0))

    #     # draw outline of maze
    #     path.addRect(
    #         0,
    #         0,
    #         self.width() - 1,
    #         self.height() - 1,
    #     )

    #     for x in range(self.__maze.size.x):
    #         currentX = x * cellSize[0]

    #         path.moveTo(
    #             QPointF(
    #                 currentX,
    #                 0,
    #             ),
    #         )

    #         path.lineTo(
    #             QPointF(
    #                 currentX,
    #                 self.height(),
    #             ),
    #         )

    #         for y in range(self.__maze.size.y):
    #             currentY = y * cellSize[1]

    #             path.moveTo(
    #                 QPointF(
    #                     0,
    #                     currentY,
    #                 )
    #             )

    #             path.lineTo(
    #                 QPointF(
    #                     self.width(),
    #                     currentY,
    #                 )
    #             )

    #     return path
