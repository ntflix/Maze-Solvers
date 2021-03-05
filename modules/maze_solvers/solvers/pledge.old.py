import logging
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from modules.maze_solvers.relative_direction import RelativeDirection
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver


class PledgeSolver(MazeSolver):
    def __init__(
        self,
        maze: MazeProtocol,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, startingDirection)

        # set our algorithmStep to 0 as we're on the 1st step of the pledge algorithm
        self._setAlgorithmStep(0)

        logging.debug(
            f"Initialized Pledge maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows:
        ```pseudocode
        > Step 0
            0   SET angle_counter to 0
        > Step 1
            1   GO forward
            2       Collision?
            3       YES:
            4               GOTO step 2
            5       NO:
            6               GOTO step 1
        > Step 2
            7   TURN right
        > Step 3
            8   FOLLOW obstacle wall
            9      IF angle_counter == 0:
            10          GOTO step 4
            11  GOTO step 3
        > Step 4
            12  IF exit found:
            13      BREAK
            14  ELSE:
            15      GOTO step 1
        ```
        """

        # initialise result var to return later on
        result = MazeSolverCommandResult(True, "", self._state)
        command = MazeSolverCommand(
            "",
            MazeSolverCommandType.detection,
            None,
        )

        algorithmStep = self._getAlgorithmStep()

        logging.info(
            f"Attempting to advance the Pledge solver. Current step: {algorithmStep}"
        )

        if algorithmStep == 0:
            # set angle_counter to 0
            self._state.solverSpecificVariables["angle_counter"] = (int, 0)
            self._setAlgorithmStep(1)

        elif algorithmStep == 1:
            movementResult = self._moveForward()
            if movementResult.success:
                # no collision
                self._setAlgorithmStep(1)
            else:
                # there was a collision
                self._setAlgorithmStep(2)

        elif algorithmStep == 2:
            self._turn(RelativeDirection.right)
            self._setAlgorithmStep(3)

        elif algorithmStep == 3:

            self._turn(RelativeDirection.left)
            wallIsForward = self._detectForward()
            if wallIsForward.obstacleExists:

        pledgeCommandResult = MazeSolverCommandResult(
            result.success,  # type: ignore  # for static type checking
            result.humanDescription,  # type: ignore  # for static type checking
            self._state,
        )

        command = MazeSolverCommand(
            humanDescription=command.humanDescription,
            commandType=command.commandType,
            commandResult=pledgeCommandResult,
        )

        # add to command history
        self._saveCommandToHistory(command)

        logging.info(
            f"{command.humanDescription}: {pledgeCommandResult.humanDescription}"
        )

        return pledgeCommandResult
