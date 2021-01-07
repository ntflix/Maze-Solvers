from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.maze_solvers.commands.commands.directionable_command import (
    DirectionableCommand,
)
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Optional, overload
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)


class MovementCommand(MazeSolverCommand, DirectionableCommand):
    """
    An agent moving in some direction.

    Conforms to:
        `MazeSolverCommand`,
        `DirectionableCommand`
    """

    # the direction it was moving in
    absoluteDirection: AbsoluteDirection

    # the cell index it started in
    cell: int

    # the human-readable description of the command
    humanDescription: str

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.movement

    # the (optional) result of the movement
    commandResult: Optional[MazeSolverCommandResult] = None

    @overload
    def __init__(self) -> None:
        self.humanDescription = ""

    def __init__(self, humanDescription: str) -> None:
        self.humanDescription = humanDescription