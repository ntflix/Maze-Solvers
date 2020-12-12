from abc import abstractclassmethod
from modules.maze_solvers.commands.protocols.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from typing import Optional, Protocol


class MazeSolverCommand(Protocol):
    """
    The protocol for any maze solver command to conform to.
    """

    # the human-readable description of the command
    humanDescription: str

    # the type, either movement or detection, of the command.
    commandType: MazeSolverCommandType

    # the result of the command. optional for if the command is not completed
    commandResult: Optional[MazeSolverCommandResult]

    @abstractclassmethod
    def __repr__(self) -> str:
        raise NotImplementedError(
            "Called `__repr__()` method on abstract class 'MazeSolverCommand'"
        )

    @abstractclassmethod
    def __init__(self) -> None:
        raise NotImplementedError(
            "Called `__init__()` method on abstract class 'MazeSolverCommand'"
        )
