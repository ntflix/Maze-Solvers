from modules.data_structures.graph.graph import Graph
from modules.data_structures.maze.maze.maze_protocol import MazeProtocol
from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from typing import Dict, Tuple


class Maze(MazeProtocol):
    """
    The Maze class.

    Conforms to:
        `MazeProtocol`
    """

    # the Graph of MazeCells representing the maze.
    __maze: Graph[MazeCell]

    __coordinates: Dict[
        MazeCell, Tuple[int, int]
    ]  # a dictionary of MazeCells and their XY coordinates in the maze

    def __init__(self, size: Tuple[int, int]) -> None:
        """Initialize a maze from a given size.
        The given maze will have all walls – i.e., no cells will have connections between them.
        This would look like a grid.

        Args:
            size (Tuple[int, int]): The XY size of the desired maze.
        """
        self.__maze = Graph[MazeCell].createSquareGraph(size[0], size[1])

        # initialize cellIndex to 0 so we can iterate over the range of cells
        cellIndex = 0
        # iterate over the X and Y of the provided maze size
        for x in range(size[0]):
            for y in range(size[1]):
                # get this maze cell from the previously initialized graph
                thisMazeCell = self.__maze[cellIndex]
                # make sure the mazeCell actually exists
                if thisMazeCell is not None:
                    # set the maze's coordinates object of this maze cell to the current X and Y
                    self.__coordinates[thisMazeCell] = (x, y)
                else:
                    # something's gone wrong and the mazeCell is None
                    raise Exception(
                        "Error while initializing maze – MazeCell at index {} was not found.".format(
                            str(cellIndex)
                        )
                    )
                cellIndex += 1
        raise NotImplementedError()

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
        """Get the coordinates of a given maze cell.

        Args:
            mazeCell (MazeCell): The maze cell whose coordinates you want to get.

        Returns:
            Tuple[int, int]: The coordinates of the given maze cell.
        """
        return self.__coordinates[mazeCell]

    def getCellAtCoordinates(self, coordinates: Tuple[int, int]) -> MazeCell:
        """Get the MazeCell at specified coordinates.

        Args:
            coordinates (Tuple[int, int]): The XY coordinates of the MazeCell.

        Returns:
            MazeCell: The MazeCell at the specified coordinates.

        Raises:
            IndexError: if `coordinates` are out of bounds.
        """
