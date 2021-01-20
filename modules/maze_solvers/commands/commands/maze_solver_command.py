from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)

from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from typing import Optional


class MazeSolverCommand:
    # the human-readable description of the command
    humanDescription: str

    # the type, either movement or detection, of the command.
    commandType: MazeSolverCommandType

    # the result of the command. optional for if the command is not completed
    commandResult: Optional[MazeSolverCommandResult]

    def __repr__(self) -> str:
        return self.humanDescription

    def __init__(
        self,
        humanDescription: str,
        commandType: MazeSolverCommandType,
        commandResult: Optional[MazeSolverCommandResult] = None,
    ) -> None:
        self.humanDescription = humanDescription
        self.commandType = commandType
        self.commandResult = commandResult
