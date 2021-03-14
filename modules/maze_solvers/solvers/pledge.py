import logging
from typing import Optional, Tuple
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

        logging.debug(
            f"Initialized Pledge maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows (adapted from [https://scratch.mit.edu/projects/104473076/]):
        ```
        turnLeft {
            solver.turnLeft();
            increment pledge_angle by 90
        }

        turnRight {
            solver.turnRight();
            increment pledge_angle by -90
        }

        if pledge_angle is not set {
            set pledge_angle to 0
        }

        ssvs.finished = false
        while (ssvs.finished is false) {
            if (solver.detectFront() is true) {
                solver.turnLeft()
                set pledge_angle to 90

                while (ssvs.pledge_angle != 0) {
                    while (solver.detectFront() is true) {
                        turnLeft()
                    }
                    solver.moveForward()
                    turnRight()
                    if (solver.detectFront() is true) {
                        turnLeft()
                    }
                }
            } else {
                solver.moveForward()
            }
        }
        print("escaped")
        solver.onEscape()
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
    ) -> Tuple[MazeSolverCommand, MazeSolverCommandResult]:

        # define some helpful methods to avoid messy code and mistakes
        def setSolverStep(step: int) -> None:
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, step)

        def getSolverStep() -> int:
            return solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY][1]

        # Pledge-specific methods for helping with angle tracking
        def setPledgeAngle(angle: int) -> None:
            solver._state.solverSpecificVariables["PledgeAngle"] = (int, angle)

        def getPledgeAngle() -> Optional[int]:
            try:
                angle = solver._state.solverSpecificVariables["PledgeAngle"][1]
                return angle
            except:
                # var not set
                return None

        def turnLeftPledge() -> MazeSolverCommandResult:
            result = solver._turn(RelativeDirection.left)
            # increment Pledge angle by 90 degrees
            angle = getPledgeAngle()
            if angle is None:
                # angle hasn't been set yet
                angle = 0

            setPledgeAngle(
                angle + 90,
            )

            return result

        def turnRightPledge() -> MazeSolverCommandResult:
            result = solver._turn(RelativeDirection.right)
            # decrement Pledge angle by 90 degrees
            angle = getPledgeAngle()
            if angle is None:
                # angle hasn't been set yet
                angle = 0

            setPledgeAngle(
                angle - 90,
            )

            return result

        # define the result of our algorithm step to return later
        result: MazeSolverCommandResult = MazeSolverCommandResult(
            False, "Something went wrong", solver._state
        )

        # define the command of our algorithm step to return later
        commandHumanDescription: str
        commandType: MazeSolverCommandType

        # check if solverStep is already set, if not, set it
        try:
            _ = getSolverStep()
        except:
            setSolverStep(0)

        logging.info(
            f"Attempting to advance the Pledge solver. Current step: {getSolverStep()}"
        )

        if getPledgeAngle() is None:
            setPledgeAngle(0)

        # and now, the actual algorithm!
        # See below this giant if-else block for a better reading of the algorithm with state comments.
        step = getSolverStep()
        if step == 0:
            if solver._state.currentCell != solver.endingPosition:
                setSolverStep(1)
            else:
                setSolverStep(11)
            # do not break after this step, so we just call the algorithm again on itself
            (command, result) = PledgeSolver.performAlgorithmOn(solver)
        elif step == 1:
            result = solver._detectForward()
            commandHumanDescription = "Detect forward"
            commandType = MazeSolverCommandType.detection

            if result.obstacleExists:
                setSolverStep(2)
            else:
                setSolverStep(10)
        elif step == 2:
            result = solver._turn(RelativeDirection.left)
            commandHumanDescription = "Turn left and set Pledge angle to 90"
            commandType = MazeSolverCommandType.movement

            setPledgeAngle(90)
            setSolverStep(3)
        elif step == 3:
            if getPledgeAngle() != 0:
                setSolverStep(4)
            else:
                # finished the while loop
                setSolverStep(0)
            # do not return from this step so call Pledge on itself again
            (command, result) = PledgeSolver.performAlgorithmOn(solver)
        elif step == 4:
            result = solver._detectForward()
            commandHumanDescription = "Detect forward"
            commandType = MazeSolverCommandType.detection

            if result.obstacleExists:
                setSolverStep(5)
            else:
                setSolverStep(6)
        elif step == 5:
            result = turnLeftPledge()
            commandHumanDescription = "Turn left & increment Pledge angle"
            commandType = MazeSolverCommandType.movement

            setSolverStep(6)
        elif step == 6:
            result = solver._moveForward()
            commandHumanDescription = "Move forward"
            commandType = MazeSolverCommandType.movement

            setSolverStep(7)
        elif step == 7:
            result = turnRightPledge()
            commandHumanDescription = "Turn right & decrement Pledge angle"
            commandType = MazeSolverCommandType.movement

            setSolverStep(8)
        elif step == 8:
            result = solver._detectForward()
            commandHumanDescription = "Detect forward"
            commandType = MazeSolverCommandType.detection

            if result.obstacleExists:
                setSolverStep(9)
            else:
                setSolverStep(0)
        elif step == 9:
            result = turnLeftPledge()
            commandHumanDescription = "Turn left & increment Pledge angle"
            commandType = MazeSolverCommandType.movement

            setSolverStep(10)
        elif step == 10:
            result = solver._moveForward()
            commandHumanDescription = "Move forward"
            commandType = MazeSolverCommandType.movement

            setSolverStep(0)
        elif step == 11:
            # finished, we are at the end position
            result = MazeSolverCommandResult(True, "Solver finished", solver._state)
            commandHumanDescription = "Finish maze"
            commandType = MazeSolverCommandType.movement

            print("BOOIIIIIIII")
            exit()

        # actual algorithm is below – but without the states
        """
        # check we've reached the end of the maze
        # s0
        while solver._state.currentCell != solver.endingPosition:
            # s1
            # detect if obstacle is in front
            if solver._detectForward().obstacleExists:
                # s2
                # something in the way; turn left.
                result = solver._turn(RelativeDirection.left)
                setPledgeAngle(90)

                # s3
                while getPledgeAngle() != 0:
                    # s4
                    while solver._detectForward().obstacleExists:
                        # s5
                        result = turnLeftPledge()
                    # s6
                    result = solver._moveForward()
                    # s7
                    result = turnRightPledge()

                    # s8
                    if solver._detectForward().obstacleExists:
                        # s9
                        result = turnLeftPledge()
            else:
                result = solver._moveForward()
                # s10

        if solver._state.currentCell == solver.endingPosition:
            # s12
            result = MazeSolverCommandResult(True, "Solver finished", solver._state)
            print("BOOIIIIIIII")
            exit()
        """

        """
        while (not in finish cell) {
            if (solver.detectFront() is true) {
                solver.turnLeft()
                set pledge_angle to 90

                while (ssvs.pledge_angle != 0) {
                    while (solver.detectFront() is true) {
                        turnLeft()
                    }
                    solver.moveForward()
                    turnRight()
                    if (solver.detectFront() is true) {
                        turnLeft()
                    }
                }
            } else {
                solver.moveForward()
            }
        }
        print("escaped")
        solver.onEscape()
        """

        commandHumanDescription = "Something"
        commandType = MazeSolverCommandType.detection

        command = MazeSolverCommand(
            humanDescription=commandHumanDescription,
            commandType=commandType,
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
