from math import floor
from modules.data_structures.graph.graph import Graph
from modules.data_structures.maze.maze.maze_protocol import MazeProtocol
from typing import Iterator, List
from modules.common_structures.xy import XY


class Maze(MazeProtocol):
    """
    The Maze class.

    Conforms to:
        `MazeProtocol`
    """

    # the Graph of ints representing the maze.
    __maze: Graph[int]

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
        self.__maze = Graph[int].createSquareGraph(size.x, size.y)

        # initialize as list of maze cells
        mazeLength = len(self.__maze)
        for cellIndex in range(mazeLength):

            # set this cell's node data to the new index
            self.__maze.setNodeData(
                index=cellIndex,
                newValue=cellIndex,
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

    def __iter__(self) -> Iterator[int]:
        for cell in self.__maze:
            data = cell.data
            if data is not None:
                yield data

    def _toGraph(self) -> Graph[int]:
        """Return a graph representation of the maze where the connections are adjacent cells without walls between and nodes are the maze cells.

        Returns:
            Graph[int]: The graph representation of the maze.
        """
        return self.__maze

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
            if self.__checkCoordinateIsValid(thisCoordinate):
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
        if not self.__checkIndexIsValid(cellIndex):
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
        Y = floor(index / self.size.x)
        X = index % self.size.x

        return XY(X, Y)

    def __checkCoordinateIsValid(self, coordinate: XY) -> bool:
        for axisValue in coordinate:
            # check it's not too small
            if axisValue < 0:
                return False

        # check it's not too big
        if coordinate.y >= self.size.y:
            return False

        if coordinate.x >= self.size.x:
            return False

        return True

    def __checkIndexIsValid(self, index: int) -> bool:
        coordinate = self.getCoordinatesFromIndex(index)
        return self.__checkCoordinateIsValid(coordinate)

    def __checkIsAdjacentWithException(self, indexA: int, indexB: int) -> bool:
        if indexB in self.getNeighboursOfCell(indexA):
            return True
        else:
            # cells not adjacent
            raise ValueError(
                f"Cell at index {indexA} is not adjacent to cell at {indexB}."
            )

    def getCoordinatesFromIndex(self, cellIndex: int) -> XY:
        """Get the coordinates of a given maze cell.

        Args:
            cellIndex (int): The maze cell's index whose coordinates you want to get.

        Returns:
            XY: The XY coordinates of the given maze cell.
        """
        # check the given index is valid
        self.__checkIndexIsValidWithException(cellIndex)

        # it is valid, so get coordinates
        return self.__getXYFromIndex(cellIndex)

    def addWallBetween(
        self,
        cellAIndex: int,
        cellBIndex: int,
        bidirectional: bool = True,
    ) -> None:
        """Add a wall between two adjacent cells.

        This works by removing a link between them in the graph.

        Args:
            cellA (int): The 'from' cell
            cellB (int): The 'to' cell
            bidirectional (bool, optional): Whether to create a bidirectional link. Defaults to True.
        """
        self.__checkIndexIsValidWithException(cellAIndex)
        self.__checkIndexIsValidWithException(cellBIndex)

        if self.__checkIsAdjacentWithException(cellAIndex, cellBIndex):
            # remove the link, which removes the lack of wall (puts something in the way between the cells)
            try:
                self.__maze.removeLinkBetween(cellAIndex, cellBIndex, bidirectional)
            except ValueError as error:
                raise ValueError(
                    (
                        "You cannot add a wall that already exists: "
                        "there is already a wall between the given cells "
                        f"{cellAIndex} and {cellBIndex}: ('{error}')."
                    )
                )

    def removeWallBetween(
        self,
        cellAIndex: int,
        cellBIndex: int,
        bidirectional: bool = True,
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
            try:
                self.__maze.addLinkBetween(cellAIndex, cellBIndex, bidirectional)
            except ValueError as error:
                raise ValueError(
                    (
                        "You cannot remove a nonexistent wall: "
                        "there is not a wall between the given cells "
                        f"{cellAIndex} and {cellBIndex}: ('{error}')."
                    )
                )

    def __checkCoordinateIsValidWithException(self, coordinate: XY) -> bool:
        if not self.__checkCoordinateIsValid(coordinate):
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
