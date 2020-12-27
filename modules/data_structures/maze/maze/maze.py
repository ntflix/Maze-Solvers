from math import floor
from modules.data_structures.graph.graph import Graph
from modules.data_structures.maze.maze.maze_protocol import MazeProtocol
from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from typing import Iterator, List, Tuple
from modules.common_structures.xy import XY


class Maze(MazeProtocol):
    """
    The Maze class.

    Conforms to:
        `MazeProtocol`
    """

    # the Graph of MazeCells representing the maze.
    __maze: Graph[MazeCell]

    size: XY

    startIndex: int
    endIndex: int

    def __init__(self, sizeX: int, sizeY: int, walls: bool = True):
        """Initialize a maze from a given size.
        The given maze will have all walls – i.e., no cells will have connections between them.
        This would look like a grid.

        Args:
            size (XY): The XY size of the desired maze.
            walls(bool, optional): Whether to create a fully connected
                maze (i.e., walls between adjacent cells). Defaults to True.
        """
        size = XY(sizeX, sizeY)

        self.size = size

        # initialize `self.__maze` to an empty graph so we can operate on it
        self.__maze = Graph[MazeCell].createSquareGraph(size.x, size.y)

        # initialize as list of maze cells
        mazeLength = len(self.__maze)
        for cellIndex in range(mazeLength):

            # set this cell's node data to a new MazeCell with index
            self.__maze.setNodeData(
                index=cellIndex,
                newValue=MazeCell(cellIndex),
            )

            if not walls:
                # list of indices for this cell's neighbours
                thisCellsNeighboursIndices: List[int] = self.getNeighboursOfCell(
                    cellIndex
                )

                # and add its neighbouring cells to the graph
                for connection in thisCellsNeighboursIndices:
                    # bidirectional FALSE because the other cell will add this one later on
                    # and we don't want multiple of the same cell in the list of neighbours
                    if not self.__maze.connectionExistsFrom(cellIndex, connection):
                        self.__maze.addLinkBetween(
                            cellIndex, connection, bidirectional=False
                        )

    def __iter__(self) -> Iterator[MazeCell]:
        for cell in self.__maze:
            data = cell.data
            if data is not None:
                yield data

    def getNeighboursOfCell(self, cellIndex: int) -> List[int]:
        """Return a list of indices of the neighbour of a cell at specified index.

        Args:
            cellIndex (int): The index of the cell whose neighbours you want.

        Returns:
            List[int]: The list of indices of its neighbours.
        """

        # check the given index is valid
        self.__checkIndexIsValidWithException(cellIndex)

        # empty list of neighbours
        thisCellsNeighboursIndices: List[int] = []

        # create (unvalidated) indices of this cell's neighbours
        coordinates = self.__getXYFromIndex(cellIndex)

        unvalidatedNeighbourCoordinates = [
            XY(coordinates.x, coordinates.y - 1),  # north
            XY(coordinates.x, coordinates.y + 1),  # south
            XY(coordinates.x - 1, coordinates.y),  # west
            XY(coordinates.x + 1, coordinates.y),  # east
        ]

        # only add the neighbours that are not out of range of maze
        for thisCoordinate in unvalidatedNeighbourCoordinates:
            # if the coordinate is valid...
            if self.__coordinateIsValid(thisCoordinate):
                # then calculate its index
                indexOfCellAtThisCoordinate = self.getIndexFromCoordinates(
                    thisCoordinate.x, thisCoordinate.y
                )
                # and add it to this cell's neighbours
                thisCellsNeighboursIndices.append(indexOfCellAtThisCoordinate)

        return thisCellsNeighboursIndices

    def getConnectionsOfCellAtIndex(self, cellIndex: int) -> List[int]:
        # check that the cellIndex is OK
        self.__checkIndexIsValidWithException(cellIndex)

        # mazeCell index is OK
        return self.__maze.getConnectionsOfNodeAtIndex(cellIndex)

    def __checkIndexIsValidWithException(self, cellIndex: int) -> bool:
        if not self.__indexIsValid(cellIndex):
            # it is not valid so raise error
            # calculate the index of the last cell in maze
            lastCellCoordinate = XY(self.size.x - 1, self.size.y - 1)
            lastCellIndex = self.getIndexFromCoordinates(
                lastCellCoordinate.x,
                lastCellCoordinate.y,
            )

            # raise appropriate error with message:
            raise IndexError(
                f"`cellIndex` out of range ({cellIndex} not between 0 and {lastCellIndex})."
            )

        return True

    def __getXYFromIndex(self, index: int) -> XY:
        """Calculate the coordinates of a cell at a given index

        Args:
            index (int): The index of the cell whose coordinates you want.

        Returns:
            XY: The coordinates of the cell.
        """
        Y = floor(index / self.size.y)
        X = index % self.size.x

        return XY(X, Y)

    def __coordinateIsValid(self, coordinate: XY) -> bool:
        for axisValue in coordinate:
            # check it's not too small
            if axisValue < 0:
                return False
            # check it's not too big
            if axisValue >= self.size.y:
                return False

        return True

    def __indexIsValid(self, index: int) -> bool:
        coordinate = self.__getXYFromIndex(index)
        return self.__coordinateIsValid(coordinate)

    def __checkIsAdjacentWithException(self, indexA: int, indexB: int) -> bool:
        if indexB in self.getNeighboursOfCell(indexA):
            return True
        else:
            # cells not adjacent
            raise ValueError(
                f"Cell at index {indexA} is not adjacent to cell at {indexB}."
            )

    def addWallBetween(
        self, cellAIndex: int, cellBIndex: int, bidirectional: bool = True
    ) -> None:
        """Add a wall between two adjacent cells.

        This works by removing a link between them in the graph.

        Args:
            cellA (MazeCell): The 'from' cell
            cellB (MazeCell): The 'to' cell
            bidirectional (bool, optional): Whether to create a bidirectional link. Defaults to True.
        """
        self.__checkIndexIsValidWithException(cellAIndex)
        self.__checkIndexIsValidWithException(cellBIndex)

        if self.__checkIsAdjacentWithException(cellAIndex, cellBIndex):
            # remove the link, which removes the lack of wall (puts something in the way between the cells)
            self.__maze.removeLinkBetween(cellAIndex, cellBIndex, bidirectional)

    def removeWallBetween(
        self, cellAIndex: int, cellBIndex: int, bidirectional: bool = True
    ) -> None:
        """Remove a wall between two adjacent cells.

        This works by adding a link between them in the graph.

        Args:
            cellA (int): The 'from' cell's index
            cellB (int): The 'to' cell's index
            bidirectional (bool, optional): Whether to remove wall in both directions. Defaults to True.
        """
        self.__checkIndexIsValidWithException(cellAIndex)
        self.__checkIndexIsValidWithException(cellBIndex)

        if self.__checkIsAdjacentWithException(cellAIndex, cellBIndex):
            self.__maze.addLinkBetween(cellAIndex, cellBIndex, bidirectional)

    def getCoordinatesFromIndex(self, cellIndex: int) -> Tuple[int, int]:
        """Get the coordinates of a given maze cell.

        Args:
            cellIndex (int): The maze cell's index whose coordinates you want to get.

        Returns:
            Tuple[int, int]: The XY coordinates of the given maze cell.
        """
        # check the given index is valid
        self.__checkIndexIsValidWithException(cellIndex)

        # it is valid, so get coordinates
        coords = self.__getXYFromIndex(cellIndex)

        # and return as Tuple[int, int] for (x, y)
        return (coords.x, coords.y)

    def __checkCoordinateIsValidWithException(self, coordinate: XY) -> bool:
        if not self.__coordinateIsValid(coordinate):
            raise ValueError(f"Coordinate {coordinate} is not valid.")
        return True

    def getIndexFromCoordinates(self, x: int, y: int) -> int:
        """Calculate the index of a cell at given coordinates

        Args:
            x: The X coordinate of the cell whose index you want.
            y: The Y coordinate of the cell whose index you want.

        Returns:
            int: The index of the cell.
        """
        # check the coords are valid
        self.__checkCoordinateIsValidWithException(XY(x, y))

        # (y * xSize) + x
        index = (y * self.size.x) + x
        return index
