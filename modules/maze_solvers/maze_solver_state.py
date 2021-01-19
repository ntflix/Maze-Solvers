from typing import Any, Dict, Tuple
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.common_structures.xy import XY


class MazeSolverState:
    # coordinate of location
    currentCell: XY

    # direction facing
    facingDirection: AbsoluteDirection

    # custom variables of the maze solver that may be presented to the user
    # for example, the Pledge algorithm has to keep track of how many turns it's done in one direction
    # so that would be something like ['leftTurns'] = [int, 2]
    # the tuple is the datatype followed by the data
    solverSpecificVariables: Dict[str, Tuple[type, Any]]
