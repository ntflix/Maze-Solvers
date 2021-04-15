from modules.maze_solvers.maze_solver_state import MazeSolverState
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
from PyQt6.QtCore import QPointF, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget


class MazeView(QWidget):
    __painter: QPainter
    __maze: MazeProtocol
    __keepAspectRatio: bool
    __solverState: Optional[MazeSolverState] = None

    onMazeSolverAgentUpdate = pyqtSignal(MazeSolverState)

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

        # connect the onMazeSolverAgentUpdate signal with our internal method
        self.onMazeSolverAgentUpdate.connect(self.__onMazeSolverAgentUpdate)

    def __onMazeSolverAgentUpdate(self, newState: MazeSolverState) -> None:
        print("__onMazeSolverAgentUpdate called in MazeView")
        self.__solverState = newState
        self.update()
        # self.__drawAgent(self.__solverState)

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

        # only draw the agent if the solverState is bound
        # if self.__solverState is not None:
        # it is a bound variable so draw it
        if self.__solverState is not None:
            agent = self.__drawAgent(self.__solverState)
            self.__painter.drawPath(agent)

        mazePath = self.__createMazePath()
        self.__painter.drawPath(mazePath)

        self.__painter.end()

    def __drawAgent(
        self,
        solverState: MazeSolverState,
    ) -> QPainterPath:
        # solverAgentPainter = QPainter(self)
        # Calculate size of each cell to be able to draw to proper scale
        cellSize = (
            self.width() / self.__maze.size.x,
            self.height() / self.__maze.size.y,
        )

        solverAgent = QPainterPath()

        # draw the agent shape
        currentPosition = (
            solverState.currentCell.x * cellSize[0],
            solverState.currentCell.y * cellSize[1],
        )

        solverAgent.addEllipse(
            currentPosition[0],
            currentPosition[1],
            cellSize[0],
            cellSize[1],
        )

        ###
        ### Draw the direction arrow of the solver
        ###
        # get the facing direction of the solver
        direction = solverState.facingDirection
        # calculte middle of agent solver sprite to draw from
        middleOfCircle = (
            currentPosition[0] + cellSize[0] * 0.5,
            currentPosition[1] + cellSize[1] * 0.5,
        )
        # calculate the XY of the edge of the circle that we want to move to (to the facing direction)
        #   start by getting the middle of the circle and then changing it accordingly
        edgeOfCircle = [
            middleOfCircle[0],
            middleOfCircle[1],
        ]
        if direction == AbsoluteDirection.north:
            # north, so take away half the circle size in the Y direction
            edgeOfCircle[1] -= cellSize[1] * 0.5
        elif direction == AbsoluteDirection.south:
            # south, so add half the circle size in the Y direction
            edgeOfCircle[1] += cellSize[1] * 0.5
        elif direction == AbsoluteDirection.west:
            # west, so take away half the circle size in the X direction
            edgeOfCircle[0] -= cellSize[0] * 0.5
        elif direction == AbsoluteDirection.east:
            # east, so add half the circle size in the X direction
            edgeOfCircle[0] += cellSize[0] * 0.5

        # move to the center of the circle
        solverAgent.moveTo(
            middleOfCircle[0],
            middleOfCircle[1],
        )
        # draw a line from the center of the circle to the facing direction edge of the circle
        solverAgent.lineTo(
            edgeOfCircle[0],
            edgeOfCircle[1],
        )

        return solverAgent

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

            for x in range(self.__maze.size.x):
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
