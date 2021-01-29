import logging
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
from modules.maze_solvers.relative_direction import RelativeDirection
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver


class WallFollower(MazeSolver):
    def __init__(
        self,
        maze: Maze,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, startingDirection)

        # set our algorithmStep to 0 as we're on the 1st step of the wall follower algorithm
        self._setAlgorithmStep(0)

        logging.debug(
            f"Initialized Wall Follower maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows:
        ```pseudocode
        > Step 0
            1   GO forward
            2       Collision?
            3           NO:
            4               GOTO #1 (if repeat)
            5           YES:
        > Step 1
            6               DETECT front
            7               IF front is not clear:
        > Step 2
            8                   TURN right
            9                   GOTO step 1
        > Step 3
            10              GO forward
        > Step 4
            11              TURN left
        > Step 5
            12              GO forward
            13                  Collision?
            14                      YES:
            15                          GOTO step 1
            16                      NO:
            17                          GOTO step 4
        ```
        """

        # initialise result var to return later on
        result = MazeSolverCommandResult(True, "", self._state)
        command = MazeSolverCommand("", MazeSolverCommandType.detection, None)

        algorithmStep = self._getAlgorithmStep()

        logging.info(
            f"Attempting to advance the Wall Follower. Current step: {algorithmStep}"
        )

        if algorithmStep == 0:
            # Go forward and detect if a collision ocurred.
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Move forward"
            # GO forward
            forward = self._moveForward()
            # check for collision
            if forward.success:
                # no collision, keep the algorithmStep the same to repeat
                result.success = True
                result.humanDescription = "Moved forward"
            else:
                # collision ocurred
                # move to step 1
                self._setAlgorithmStep(1)
                result.success = False
                result.humanDescription = (
                    "Detected collision while attempting to move forward"
                )

        elif algorithmStep == 1:
            # Check front is clear.
            # UNTIL no obstacle is in front (implicit loop through algorithmStep remaining the same)
            result.success = True
            command.commandType = MazeSolverCommandType.detection
            command.humanDescription = "Detect obstacle in front"

            if self._detectForward().obstacleExists:
                #  goto step 2
                self._setAlgorithmStep(2)
                result.humanDescription = "Detected obstacle in front"
            else:
                # nothing in the way, goto step 3
                self._setAlgorithmStep(3)
                result.humanDescription = "Nothing detected in front"

        elif algorithmStep == 2:
            # Turn right, go to step 1.
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Turn right"
            # TURN right
            self._turn(RelativeDirection.right)
            # go back to detecting (step 1)
            self._setAlgorithmStep(1)
            result.success = True
            result.humanDescription = (
                f"Turned right to face {self._state.facingDirection}"
            )

        elif algorithmStep == 3:
            # Just go forward.
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Move forward"
            # GO forward
            forward = self._moveForward()
            # goto step 4 where we turn left
            self._setAlgorithmStep(4)
            result.success = True
            result.humanDescription = "Moved forward"

        elif algorithmStep == 4:
            # Turn left
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Turn left"
            # Actually turn left
            self._turn(RelativeDirection.left)
            self._setAlgorithmStep(5)
            result.success = True
            result.humanDescription = "Turned left"

        elif algorithmStep == 5:
            # Go forward and detect collision
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Move forward"

            forward = self._moveForward()
            if forward.success:
                # GOTO step 4 where we turn left again
                self._setAlgorithmStep(4)
                result.success = True
                result.humanDescription = "Moved forward"
            else:
                # GOTO step 1 where we turn right for a bit
                self._setAlgorithmStep(1)
                result.success = False
                result.humanDescription = (
                    "Detected collision while attempting to move forward"
                )

        wallFollowerCommandResult = MazeSolverCommandResult(
            result.success,  # type: ignore  # for static type checking
            result.humanDescription,  # type: ignore  # for static type checking
            self._state,
        )

        command = MazeSolverCommand(
            humanDescription=command.humanDescription,
            commandType=command.commandType,
            commandResult=wallFollowerCommandResult,
        )

        # add to command history
        self._saveCommandToHistory(command)

        logging.info(
            f"{command.humanDescription}: {wallFollowerCommandResult.humanDescription}"
        )

        return wallFollowerCommandResult
