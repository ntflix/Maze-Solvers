from modules.maze_solvers.relative_direction import RelativeDirection
from modules.maze_solvers.commands.command_types.maze_solver_command_type import (
    MazeSolverCommandType,
)
from modules.maze_solvers.commands.command_types.command_protocol import (
    MazeSolverCommand,
)


class MovementCommand(MazeSolverCommand):
    """
    A subclass of MazeSolverCommand used to specify an agent moving in some direction.
    """

    direction: RelativeDirection  # the direction of movement

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.movement