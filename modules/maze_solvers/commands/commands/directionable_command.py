from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Protocol


class DirectionableCommand(Protocol):
    # the absolute direction of the action
    absoluteDirection: AbsoluteDirection

    # the cell index the action happened was called in
    cell: int
