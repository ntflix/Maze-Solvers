from abc import abstractclassmethod
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from typing import Protocol


class MazeSolverProtocol(Protocol):
    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def advance(self) -> MazeSolverCommandResult:
        pass
