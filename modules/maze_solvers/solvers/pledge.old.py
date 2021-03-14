import logging
from typing import Tuple
from modules.maze_solvers.solvers.wall_follower import WallFollower
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


PLEDGESOLVERSTEP_KEY = "pledgeSolverStep"


class PledgeSolver(MazeSolver):
    def __init__(
        self,
        maze: MazeProtocol,
        startingPosition: XY,
        endingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, endingPosition, startingDirection)

        # set our algorithmStep to 0 as we're on the 1st step of the pledge algorithm
        self._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 0)

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
            4           GOTO step 2
            5       NO:
            6           GOTO step 1
        > Step 2
            7   TURN right (& increment angle counter)
        > Step 3
            8   FOLLOW obstacle wall (& mutate angle counter appropriately)
        > Step 4
            9      IF angle_counter == 0:
            10          GOTO step 5
            11     ELSE: GOTO step 3
        > Step 5
            12  IF exit found:
            13      BREAK
            14  ELSE:
            15      GOTO step 1
        ```
        """

        # use this class' static performAlgorithm method to do heavy lifting
        command, pledgeCommandResult = self.performAlgorithmOn(self)

        # add to command history
        self._saveCommandToHistory(command)

        logging.info(
            f"{command.humanDescription}: {pledgeCommandResult.humanDescription}"
        )

        return pledgeCommandResult

    @staticmethod
    def performAlgorithmOn(
        solver: "MazeSolver",
    ) -> Tuple[MazeSolverCommand, MazeSolverCommandResult]:

        # initialise result var to return later on
        result = MazeSolverCommandResult(True, "", solver._state)
        command = MazeSolverCommand(
            "",
            MazeSolverCommandType.detection,
            None,
        )

        algorithmStep = solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY][1]

        logging.info(
            f"Attempting to advance the Pledge solver. Current step: {algorithmStep}"
        )

        # Step 0
        #   SET angle_counter to 0
        if algorithmStep == 0:
            # set angle_counter to 0
            solver._state.solverSpecificVariables["angle_counter"] = (int, 0)
            # set the solver step to 1
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 1)
            # just assigning a variable doesn't really count as a step. therefore we call advance() again on the solver so it does something visual.
            # result = solver.advance() # disabled due to issues debugging on a different stack level

        #  Step 1
        #   GO forward
        #       Collision?
        #       YES:
        #           GOTO step 2
        #       NO:
        #           GOTO step 1
        elif algorithmStep == 1:
            result = solver._moveForward()
            if result.success:
                # no collision
                solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 1)
            else:
                # there was a collision
                solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 2)

        #  Step 2
        # TURN right
        elif algorithmStep == 2:
            result = solver._turn(RelativeDirection.right)
            # increment angle counter
            solver._state.solverSpecificVariables["angle_counter"] = (
                int,  # type of data is `int`
                (
                    solver._state.solverSpecificVariables["angle_counter"][1] + 1
                ),  # simply get the current angle and add 1
            )
            #  go to step 3
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 3)

        #  Step 3
        # FOLLOW obstacle wall
        # GOTO step 3.5
        elif algorithmStep == 3:
            # FOLLOW obstacle wall. This is stateful and therefore
            #   we must keep track of the wall follower state.
            # We can follow a wall really easily by just using the
            #   existing code of the wall follower. How
            #   cool is that!? Benefits of sticking to SOLID ;)
            ######
            # get the old facing direction so we can calculate the direction change (for the angle counter)
            oldDirection = solver.getCurrentState().facingDirection
            #  perform the wall follower
            command, result = WallFollower.performAlgorithmOn(solver)
            # get new facing direction
            newDirection = result.newState.facingDirection
            # calculate the change of direction (in degrees
            directionChangeDegrees = newDirection.toDegrees() - oldDirection.toDegrees()
            # change angle counter by direction change
            numberOfRightAnglesTurned: int = directionChangeDegrees // 90
            # mutate the `angle_counter` by the change in right angles (eg, if -1 numberOfRightAnglesTurned, decrement the counter)
            solver._state.solverSpecificVariables["angle_counter"] = (
                int,
                solver._state.solverSpecificVariables["angle_counter"][1]
                + numberOfRightAnglesTurned,
            )
            # set step to 4, to check angles
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 4)

        # Step 4
        # IF angle_counter == 0:
        #   GOTO step 5
        # ELSE:
        #   GOTO step 3
        elif algorithmStep == 4:
            #  if there are no outstanding angles to turn
            if solver._state.solverSpecificVariables["angle_counter"][1] == 0:
                # GOTO step 5
                solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 5)
            else:
                # GOTO step 3
                solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 3)

        #  Step 5
        # IF exit found:
        #   BREAK
        # ELSE:
        # GOTO step 1
        elif algorithmStep == 5:
            # if exit found:
            #   break!
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 1)

        result = MazeSolverCommandResult(
            result.success,  # type: ignore  # for static type checking
            result.humanDescription,  # type: ignore  # for static type checking
            solver._state,
        )

        command = MazeSolverCommand(
            humanDescription=command.humanDescription,
            commandType=command.commandType,
            commandResult=result,
        )

        return (command, result)


if __name__ == "__main__":
    # Test out the Pledge maze solver
    from modules.data_structures.maze.maze import Maze

    maze = Maze(10, 10, False)
    pledge = PledgeSolver(maze, XY(0, 0), XY(9, 9))

    FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
    LEVEL = 0
    logging.basicConfig(format=FORMAT, level=LEVEL)
    logging.getLogger().setLevel(LEVEL)
    log = logging.getLogger()

    while True:
        pledge.advance()
        print(pledge.getCurrentState().currentCell)
