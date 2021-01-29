#!python3.9

"""
From http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm:

- Initialize the cells of the first row to each exist in their own set.
- Now, randomly join adjacent cells, but only if they are not in the same set. When joining adjacent cells, merge the cells of both sets into a single set, indicating that all cells in both sets are now connected (there is a path that connects any two cells in the set).
- For each set, randomly create vertical connections downward to the next row. Each remaining set must have at least one vertical connection. The cells in the next row thus connected must share the set of the cell above them.
- Flesh out the next row by putting any remaining cells into their own sets.
- Repeat until the last row is reached.
- For the last row, join all adjacent cells that do not share a set, and omit the vertical connections, and you’re done!
"""

from modules.common_structures.xy import XY
from typing import List
from modules.data_structures.maze.maze import Maze


class Eller:  # TODO: Conform to MazeGenerator
    size: XY
    __maze: Maze

    def __init__(self, x: int, y: int) -> None:
        if (x <= 0) or (y <= 0):
            raise ValueError("`x` and `y` arguments must be greater than 0.")

        self.x = x
        self.y = y

    def generate(self) -> Maze:
        # First, we create an empty row of cells where each cell is in its own set.
        row = self.__makeEmptyRow()
        # Next, randomly join adjacent cells which belong to different sets.
        # The cells we join are merged into the same set.
        for i in range(len(row) - 1):
            if row[i] != row[i + 1]:
                # the two cells are not in the same set

    def __makeEmptyRow(self) -> List[int]:
        """Generate an empty row of cells for the first row of a maze.

        Returns:
            List[int]: The list of cells in the row, where the index of the value refers to its column, and the value is its set.

        Example:
            This empty row (where the number is the set #)
                .___.___.___.___.___.
                | 1 | 2 | 3 | 4 | 5 |
            Would be this list:
                [1, 2, 3, 4, 5]
        """

        # make a list
        row = [(i + 1) for i in range(self.size.x)]
        return row