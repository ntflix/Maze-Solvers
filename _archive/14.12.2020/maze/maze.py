from math import floor
from modules.data_structures.graph.graph import Graph
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from typing import Iterator, List
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

    def __init__(self, sizeX: int, sizeY: int, fullyConnected: bool = False):
        """Initialize a maze from a given size.
        The given maze will have all walls – i.e., no cells will have connections between them.
        This would look like a grid.

        Args:
            size (XY): The XY size of the desired maze.
            fullyConnected(bool, optional): Whether to create a fully connected
                maze (i.e., no walls between adjacent cells). Defaults to False.
        """
        size = XY(sizeX, sizeY)

        self.size = size

        # initialize `self.__maze` to an empty graph so we can operate on it
        self.__maze = Graph[MazeCell].createSquareGraph(size.x, size.y)

        # initialize as list of maze cells
        for cellIndex in range(len(self.__maze)):

            # set this cell's node data to a new MazeCell with index
            self.__maze.setNodeData(
                index=cellIndex,
                newValue=MazeCell(cellIndex),
            )

            if fullyConnected:
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
        # empty list of neighbours
        thisCellsNeighboursIndices: List[int] = []

        # create (unvalidated) indices of this cell's neighbours
        coordinates = self.__getCoordinateFromIndex(cellIndex)

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
                indexOfCellAtThisCoordinate = self.__getIndexFromCoordinate(
                    thisCoordinate
                )
                # and add it to this cell's neighbours
                thisCellsNeighboursIndices.append(indexOfCellAtThisCoordinate)

        return thisCellsNeighboursIndices

    def __getIndexFromCoordinate(self, coordinate: XY) -> int:
        """Calculate the index of a cell at given coordinates

        Args:
            coordinate (XY): The coordinate of the cell whose index you want.

        Returns:
            int: The index of the cell.
        """
        # (y * xSize) + x
        index = (coordinate.y * self.size.x) + coordinate.x
        return index

    def __getCoordinateFromIndex(self, index: int) -> XY:
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

    def addWallBetween(
        self, cellA: MazeCell, cellB: MazeCell, bidirectional: bool = True
    ) -> None:
        """Add a wall between two adjacent cells.

        This works by removing a link between them in the graph.

        Args:
            cellA (MazeCell): The 'from' cell
            cellB (MazeCell): The 'to' cell
            bidirectional (bool, optional): Whether to create a bidirectional link. Defaults to True.
        """

    def removeWallBetween(
        self, cellA: MazeCell, cellB: MazeCell, bidirectional: bool = True
    ) -> None:
        """Remove a wall between two adjacent cells.

        This works by adding a link between them in the graph.

        Args:
            cellA (MazeCell): The 'from' cell
            cellB (MazeCell): The 'to' cell
            bidirectional (bool, optional): Whether to remove wall in both directions. Defaults to True.
        """

    def getCoordinatesOf(self, mazeCell: MazeCell) -> XY:
        """Get the coordinates of a given maze cell.

        Args:
            mazeCell (MazeCell): The maze cell whose coordinates you want to get.

        Returns:
            XY: The coordinates of the given maze cell.
        """
        return self.__getCoordinateFromIndex(mazeCell.index)

    def getCellAtCoordinates(self, coordinates: XY) -> MazeCell:
        """Get the MazeCell at specified coordinates.

        Args:
            coordinates (XY): The XY coordinates of the MazeCell.

        Returns:
            MazeCell: The MazeCell at the specified coordinates.

        Raises:
            IndexError: if `coordinates` are out of bounds.
        """
