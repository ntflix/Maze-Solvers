from modules.maze_solvers.commands.commands.directionable_command import (
    DirectionableCommand,
)
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Optional
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)


class DetectionCommand(MazeSolverCommand, DirectionableCommand):
    """
    An agent detecting something.

    Conforms to:
        `MazeSolverCommand`,
        `DirectionableCommand`
    """

    # the cell it is in
    cell: XY

    # the absolute direction it is detecting in
    absoluteDirection: AbsoluteDirection

    # the human-readable description of the command
    humanDescription: str

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.detection

    # the result of the detection
    commandResult: Optional[MazeSolverCommandResult] = None
