import logging
import random
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver


class RandomMouse(MazeSolver):
    def __init__(
        self,
        maze: Maze,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, startingDirection)

        # set our algorithmStep to 0 as we're on the 1st step of the wall follower algorithm
        self.__setAlgorithmStep(0)

        logging.debug(
            f"Initialized Random Mouse maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows:
        ```pseudocode
        > Step 0
            1   TURN random direction
            2   MOVE forward
        ```
        """

        algorithmStep = self._state.solverSpecificVariables["algorithmStep"][1]

        logging.info(
            f"Attempting to advance the Random Mouse. Current step: {algorithmStep}"
        )

        # choose random direction to go in
        # absolute direction is less expensive than relative
        movementDirection = random.choice(AbsoluteDirection.allCases())
        self._turnAbsolute(movementDirection)
        forward = self._moveForward()

        result = MazeSolverCommandResult(
            forward.success,
            f"Turned {movementDirection} and attempted to move forward",
            self._state,
        )

        command = MazeSolverCommand(
            "Move randomly",
            MazeSolverCommandType.movement,
            result,
        )

        # add to command history
        self._saveCommandToHistory(command)

        logging.info(f"{command.humanDescription}: {result.humanDescription}")

        return result

    def __setAlgorithmStep(self, stage: int) -> None:
        """Set the step stage of the wall follower algorithm agent.

        Args:
            stage (int): The stage to set it to.
        """
        self._state.solverSpecificVariables["algorithmStep"] = (int, stage)
