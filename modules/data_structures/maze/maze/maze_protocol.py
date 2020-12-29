from modules.data_structures.graph.graph import Graph
from typing import Iterator, List, Protocol
from modules.common_structures.xy import XY


class MazeProtocol(Protocol):
    """The protocol for any Maze object to conform to.

    Args:
        Protocol ([type]): [description]
    """

    size: XY

    startIndex: int
    endIndex: int

    def __init__(self, sizeX: int, sizeY: int, fullyConnected: bool = False) -> None:
        """Initialize a maze from a given size.
        The given maze will have all walls – i.e., no cells will have connections between them.
        This would look like a grid.

        Args:
            size (XY): The XY size of the desired maze.
            fullyConnected(bool, optional): Whether to create a fully connected
                maze (i.e., no walls between adjacent cells). Defaults to False.
        """
        raise NotImplementedError()

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError()

    def _toGraph(self) -> Graph[int]:
        """Return a graph representation of the maze where the connections are adjacent cells without walls between and nodes are the maze cells.

        Returns:
            Graph[int]: The graph representation of the maze.
        """
        raise NotImplementedError()

    def getConnectionsOfCellAtIndex(self, cellIndex: int) -> List[int]:
        """Return a list of indices of the connections of a cell at given index.

        Args:
            cellIndex (int): The index of the cell whose connections you want.

        Returns:
            List[int]: List of connections.
        """
        raise NotImplementedError()

    def getNeighboursOfCell(self, cellIndex: int) -> List[int]:
        """Return a list of indices of the neighbour of a cell at specified index.

        Args:
            cellIndex (int): The index of the cell whose neighbours you want.

        Returns:
            List[int]: The list of indices of its neighbours.
        """
        raise NotImplementedError()

    def addWallBetween(
        self, cellAIndex: int, cellBIndex: int, bidirectional: bool = True
    ) -> None:
        """Add a wall between two adjacent cells.

        This works by removing a link between them in the graph.

        Args:
            cellA (int): The 'from' cell
            cellB (int): The 'to' cell
            bidirectional (bool, optional): Whether to create a bidirectional link. Defaults to True.
        """
        raise NotImplementedError()

    def removeWallBetween(
        self, cellAIndex: int, cellBIndex: int, bidirectional: bool = True
    ) -> None:
        """Remove a wall between two adjacent cells.

        This works by adding a link between them in the graph.

        Args:
            cellA (int): The 'from' cell
            cellB (int): The 'to' cell
            bidirectional (bool, optional): Whether to remove wall in both directions. Defaults to True.
        """
        raise NotImplementedError()

    def getCoordinatesFromIndex(self, cellIndex: int) -> XY:
        """Get the coordinates of a given maze cell.

        Args:
            cellIndex (int): The maze cell's index whose coordinates you want to get.

        Returns:
            XY: The XY coordinates of the given maze cell.
        """
        raise NotImplementedError()

    def getIndexFromCoordinates(self, x: int, y: int) -> int:
        """Get the int at specified coordinates.

        Args:
            x (int): The X coordinate of the int.
            y (int): The Y coordinate of the int.

        Returns:
            int: The int index at the specified coordinates.
        """
        raise NotImplementedError()
