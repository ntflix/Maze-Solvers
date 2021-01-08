from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Protocol


class DirectionableCommand(Protocol):
    # the absolute direction of the action
    absoluteDirection: AbsoluteDirection

    # the cell coordinate that the action that happened was called in
    cell: XY
