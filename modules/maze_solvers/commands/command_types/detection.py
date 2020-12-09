from modules.maze_solvers.relative_direction import RelativeDirection
from modules.maze_solvers.commands.command_types.maze_solver_command_type import (
    MazeSolverCommandType,
)
from modules.maze_solvers.commands.command_types.command_protocol import (
    MazeSolverCommand,
)


class DetectionCommand(MazeSolverCommand):
    """
    A subclass of MazeSolverCommand used to specify an agent detecting something.
    """

    direction: RelativeDirection  # the direction it is detecting in

    # set the commandType inherited from super:
    commandType = MazeSolverCommandType.detection
