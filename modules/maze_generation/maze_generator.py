from modules.data_structures.maze.maze import Maze
from modules.common_structures.xy import XY
from typing import Protocol


class MazeGenerator(Protocol):
    def __init__(self, size: XY) -> None:
        """Constructor for a MazeGenerator.

        Args:
            size (XY): The XY size of the desired maze.
        """
        raise NotImplementedError()

    def generate(self) -> Maze:
        """Generate the maze with a given start position.

        Returns:
            Maze: The generated maze.
        """
        raise NotImplementedError()

    def _testSizeIsValidWithException(self, size: XY) -> None:
        """Check that a given size for a maze is valid. A valid maze size is at least 1 in each dimension (X and Y).

        Parameters
        ----------
        size : XY
            The given size.

        Raises
        ------
        ValueError
            Size is invalid.
        """
        valid = True

        # size must be at least (1, 1)
        if size.toTuple()[0] <= 1:
            valid = False
        elif size.toTuple()[1] <= 1:
            valid = False

        if not valid:
            raise ValueError("Maze size must be at least (1, 1) in each dimension.")
