from modules.maze_solvers.maze_solver_state import MazeSolverState
from typing import Protocol


class MazeSolverCommandResult(Protocol):
    humanDescription: str
    newState: MazeSolverState

    def __init__(
        self,
        humanDescription: str,
        state: MazeSolverState,
    ) -> None:
        pass

    def __repr__(self) -> str:
        return self.humanDescription
