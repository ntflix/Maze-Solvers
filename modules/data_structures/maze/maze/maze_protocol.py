from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from typing import Iterator, List, Protocol, Tuple
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

    def __iter__(self) -> Iterator[MazeCell]:
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
            cellA (MazeCell): The 'from' cell
            cellB (MazeCell): The 'to' cell
            bidirectional (bool, optional): Whether to create a bidirectional link. Defaults to True.
        """
        raise NotImplementedError()

    def removeWallBetween(
        self, cellAIndex: int, cellBIndex: int, bidirectional: bool = True
    ) -> None:
        """Remove a wall between two adjacent cells.

        This works by adding a link between them in the graph.

        Args:
            cellA (MazeCell): The 'from' cell
            cellB (MazeCell): The 'to' cell
            bidirectional (bool, optional): Whether to remove wall in both directions. Defaults to True.
        """
        raise NotImplementedError()

    def getCoordinatesOf(self, cellIndex: int) -> Tuple[int, int]:
        """Get the coordinates of a given maze cell.

        Args:
            cellIndex (int): The maze cell's index whose coordinates you want to get.

        Returns:
            Tuple[int, int]: The XY coordinates of the given maze cell.
        """
        raise NotImplementedError()

    def getCellAtCoordinates(self, x: int, y: int) -> int:
        """Get the MazeCell at specified coordinates.

        Args:
            x (int): The X coordinate of the MazeCell.
            y (int): The Y coordinate of the MazeCell.

        Returns:
            int: The MazeCell index at the specified coordinates.
        """
        raise NotImplementedError()
