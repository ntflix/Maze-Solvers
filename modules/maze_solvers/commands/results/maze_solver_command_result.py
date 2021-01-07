from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Protocol


class MazeSolverCommandResult(Protocol):
    humanDescription: str
    facing: AbsoluteDirection

    def __init__(
        self,
        humanDescription: str,
        facing: AbsoluteDirection,
    ) -> None:
        pass

    def __repr__(self) -> str:
        return self.humanDescription
