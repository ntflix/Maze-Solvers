from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from modules.data_structures.graph.graph import Graph
from typing import Protocol, Tuple


class MazeProtocol(Protocol):
    """The protocol for any Maze object to conform to.

    Args:
        Protocol ([type]): [description]
    """

    __maze: Graph[MazeCell]  # type:ignore      # ignore 'variable not accessed' error

    def __init__(self, size: Tuple[int, int]) -> None:
        """Initialize a maze from a given size.
        The given maze will have no empty walls – i.e., no cells will have connections between them.
        This would look like a grid.

        Args:
            size (Tuple[int, int]): The XY size of the desired maze.
        """

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

    def getCoordinatesOf(self, mazeCell: MazeCell) -> Tuple[int, int]:
        """Get the coordinates of a given maze cell

        Args:
            mazeCell (MazeCell): The maze cell whose coordinates you want to get.

        Returns:
            Tuple[int, int]: The coordinates of the given maze cell.
        """