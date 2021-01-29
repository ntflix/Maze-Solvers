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