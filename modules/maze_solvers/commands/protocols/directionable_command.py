from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from modules.maze_solvers.relative_direction import RelativeDirection
from typing import Protocol


class DirectionableCommand(Protocol):
    # the relative direction of action
    relativeDirection: RelativeDirection

    # the absolute direction of action
    absoluteDirection: AbsoluteDirection

    # the cell it started in
    cell: MazeCell