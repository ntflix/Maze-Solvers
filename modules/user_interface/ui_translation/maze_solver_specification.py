from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver
from typing import Type
from modules.common_structures.xy import XY


class MazeSolverSpecification:
    startPosition: XY
    endPosition: XY
    solverType: Type[MazeSolver]

    def __init__(
        self, startPosition: XY, endPosition: XY, solverType: Type[MazeSolver]
    ) -> None:
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.solverType = solverType