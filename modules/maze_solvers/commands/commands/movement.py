from modules.maze_solvers.commands.protocols.directionable_command import (
    DirectionableCommand,
)
from modules.data_structures.maze.maze_cell.maze_cell import MazeCell
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from typing import Optional, overload
from modules.maze_solvers.commands.results.movement_command_result import (
    MovementCommandResult,
)
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from modules.maze_solvers.commands.protocols.command_protocol import MazeSolverCommand
from modules.maze_solvers.relative_direction import RelativeDirection


class MovementCommand(MazeSolverCommand, DirectionableCommand):
    """
    An agent moving in some direction.

    Conforms to:
        `MazeSolverCommand`,
        `DirectionableCommand`
    """

    # the relative direction of movement
    relativeDirection: RelativeDirection

    # the direction it was moving in
    absoluteDirection: AbsoluteDirection

    # the cell it started in
    cell: MazeCell

    # the human-readable description of the command
    humanDescription: str

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.movement

    # the (optional) result of the movement
    commandResult: Optional[MovementCommandResult] = None

    @overload
    def __init__(self) -> None:
        self.humanDescription = ""

    def __init__(self, humanDescription: str) -> None:
        self.humanDescription = humanDescription