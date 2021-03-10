import logging
from typing import Tuple
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
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, startingDirection)

        # set our algorithmStep to 0 as we're on the 1st step of the pledge algorithm
        # self._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 0)

        logging.debug(
            f"Initialized Pledge maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows:
        ```
        SOLVER.VARS["TOTAL_TURNS"] = 0

        TURN_LEFT() {
            SOLVER.VARS["TOTAL_TURNS"] += 90
            SOLVER.TURN_LEFT()
        }

        TURN_RIGHT() {
            SOLVER.VARS["TOTAL_TURNS"] -= 90
            SOLVER.TURN_RIGHT()
        }

        ~~~~~~~~~~~~~~~~~~~~~
        #0 ~~~~~~~~~~~~~~~~~~
        MOVE FORWARD
            SUCCESS
                GOTO #0
            FAILURE
                GOTO #1
        #1 ~~~~~~~~~~~~~~~~~~
        TURN_LEFT()
        WHILE SOLVER.VARS["TOTAL_TURNS"] IS NOT 0:
            PLEDGE_SOLVER.PERFORM_ON(SOLVER)
        GOTO #0
        ~~~~~~~~~~~~~~~~~~~~~
        ~~~~~~~~~~~~~~~~~~~~~
        ```
        From [http://www.scratch-blog.com/2013/10/the-pledge-maze-solving-algorithm.html]:
            [Pledge's] algorithm collects local information by adding turns to the left as positive numbers and turns to the right as negative values to a variable called Total Turning.
            Total Turning is initially set to zero. The robot then moves forward until it strikes a barrier. It turns left, adding the angle measure of the turn to Total Turning and then executes the rest of the algorithm until Total Turning equals zero degrees (not 360º) that indicates the robot has navigated around the barrier. The algorithm resets Total Turning to zero, and the robot again moves forward until it strikes another barrier. And so on.
            A complete discussion of the Pledge algorithm can be found in the book Turtle Geometry, by Harold Abelson and Andrea A. diSessa published by the MIT Press in 1980.
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
        recursionLevel: int = 0,
    ) -> Tuple[MazeSolverCommand, MazeSolverCommandResult]:

        # initialise result var to return later on
        result = MazeSolverCommandResult(True, "", solver._state)
        command = MazeSolverCommand(
            "",
            MazeSolverCommandType.detection,
            None,
        )
        algorithmStep: int
        try:
            algorithmStep = solver._state.solverSpecificVariables[
                # the key, for example, may be "pledgeSolverStep0" for the 0th recursion level
                f"{PLEDGESOLVERSTEP_KEY}{recursionLevel}"
            ][1]
        except:
            # new recursion level, so make new PledgeSolverStep (start at 0, of course)
            solver._state.solverSpecificVariables[
                # the key, for example, may be "pledgeSolverStep0" for the 0th recursion level
                f"{PLEDGESOLVERSTEP_KEY}{recursionLevel}"
            ] = (int, 0)
            algorithmStep = 0

        try:
            _ = solver._state.solverSpecificVariables[f"TOTAL_TURNS{recursionLevel}"][1]
        except:
            solver._state.solverSpecificVariables[f"TOTAL_TURNS{recursionLevel}"] = (
                int,
                0,
            )

        logging.info(
            f"Attempting to advance the Pledge solver. Current step: {algorithmStep}"
        )

        ###
        # 0 ~~~~~~~~~~~~~~~~~~
        # MOVE FORWARD
        #     SUCCESS
        #         GOTO #0
        #     FAILURE
        #         GOTO #1
        ###
        if algorithmStep == 0:
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Move forward"
            result = solver._moveForward()
            if result.success:
                solver._state.solverSpecificVariables[
                    f"{PLEDGESOLVERSTEP_KEY}{recursionLevel}"
                ] = (int, 0)
            else:
                solver._state.solverSpecificVariables[
                    f"{PLEDGESOLVERSTEP_KEY}{recursionLevel}"
                ] = (int, 1)
        ###
        # 1 ~~~~~~~~~~~~~~~~~~
        # TURN_LEFT()
        # WHILE SOLVER.VARS["TOTAL_TURNS"] IS NOT 0:
        #     PLEDGE_SOLVER.PERFORM_ON(SOLVER)
        # GOTO #0
        ###
        elif algorithmStep == 1:
            command.commandType = MazeSolverCommandType.movement
            command.humanDescription = "Turn left & perform Pledge recursively"
            # decrement TOTAL_TURNS by 90 degrees
            solver._state.solverSpecificVariables[f"TOTAL_TURNS{recursionLevel}"] = (
                int,
                solver._state.solverSpecificVariables[f"TOTAL_TURNS{recursionLevel}"][1]
                - 90,
            )
            result = solver._turn(RelativeDirection.left)
            #  check if the subsolver is instantiated – if not, instantiate it.
            try:
                _ = solver._state.solverSpecificVariables[
                    f"SubSolverLevel{recursionLevel + 1}"
                ][1]
            except:
                solver._state.solverSpecificVariables[
                    f"SubSolverLevel{recursionLevel + 1}"
                ] = (
                    MazeSolver,  # data type
                    PledgeSolver(
                        solver._maze,
                        startingPosition=solver.getCurrentState().currentCell,
                        startingDirection=solver.getCurrentState().facingDirection,
                    ),  # actual data
                )

            while (
                solver._state.solverSpecificVariables[f"TOTAL_TURNS{recursionLevel}"][1]
                != 0
            ):
                #  perform the Pledge subsolver until TOTAL_TURNS is 0, with one higher recursion level
                result = solver._state.solverSpecificVariables[
                    f"SubSolverLevel{recursionLevel + 1}"
                ][1].advance()

            # set step back to 0
            solver._state.solverSpecificVariables[
                f"{PLEDGESOLVERSTEP_KEY}{recursionLevel}"
            ] = (int, 0)

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
    pledge = PledgeSolver(maze, XY(0, 0))

    FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
    LEVEL = 0
    logging.basicConfig(format=FORMAT, level=LEVEL)
    logging.getLogger().setLevel(LEVEL)
    log = logging.getLogger()

    while True:
        pledge.advance()
        print(pledge.getCurrentState().currentCell)
