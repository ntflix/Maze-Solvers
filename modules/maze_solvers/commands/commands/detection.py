from modules.maze_solvers.commands.protocols.directionable_command import (
    DirectionableCommand,
)
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.maze_solvers.commands.results.detection_command_result import (
    DetectionCommandResult,
)
from typing import Optional
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from modules.maze_solvers.commands.protocols.command_protocol import MazeSolverCommand
from modules.maze_solvers.relative_direction import RelativeDirection


class DetectionCommand(MazeSolverCommand, DirectionableCommand):
    """
    An agent detecting something.

    Conforms to:
        `MazeSolverCommand`,
        `DirectionableCommand`
    """

    # the relative direction it is detecting in
    relativeDirection: RelativeDirection

    # the cell index it is in
    cell: int

    # the absolute direction it is detecting in
    absoluteDirection: AbsoluteDirection

    # the human-readable description of the command
    humanDescription: str

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.detection

    # the result of the detection
    commandResult: Optional[DetectionCommandResult] = None
