from typing import Any, Dict, Tuple
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.common_structures.xy import XY


class MazeSolverState:
    # coordinate of location
    def getCurrentCell(self) -> XY:
        raise NotImplementedError()

    def getFacingDirection(self) -> AbsoluteDirection:
        raise NotImplementedError()

    # custom variables of the maze solver that may be presented to the user
    # for example, the Pledge algorithm has to keep track of how many turns it's done in one direction
    # so that would be something like ['leftTurns'] = [int, 2]
    # the tuple is the datatype followed by the data
    def getSolverSpecificVariables(self) -> Dict[str, Tuple[type, Any]]:
        raise NotImplementedError()
