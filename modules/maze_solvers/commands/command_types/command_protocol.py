from modules.maze_solvers.commands.command_types.maze_solver_command_type import (
    MazeSolverCommandType,
)
from typing import Protocol


class MazeSolverCommand(Protocol):
    """
    The protocol for any maze solver command to conform to.
    """

    humanDescription: str
    commandType: MazeSolverCommandType
    commandResult: MazeSolverCommandResult

    def __repr__(self):
        return self.humanDescription