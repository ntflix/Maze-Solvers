import logging
from modules.maze_solvers.solvers.wall_follower import WallFollower
from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
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
        endingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, endingPosition, startingDirection)

        #  init Pledge vars
        # start in step 1
        self._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 1)
        # start with angle 0
        self._state.solverSpecificVariables["pledgeAngle"] = (int, 0)

        logging.debug(
            f"Initialized Pledge maze solver with maze {maze}, starting position {startingPosition} and starting direction {startingDirection}."
        )

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.
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

        commandHumanDescription: str
        commandType: MazeSolverCommandType
        result: MazeSolverCommandResult

        """
        Pledge’s algorithm

        1 Set angle counter to 0;
        2 repeat
        3   repeat
        4       Walk straight ahead;
        5   until wall hit;
        6   Turn right;
        7   repeat
        8       Follow the obstacle’s wall;
        9   until angle counter = 0;
        10 until exit found;

        Klein R., Kamphans T. (2011) Pledge's Algorithm - How to Escape from a Dark Maze. In: Vöcking B. et al. (eds) Algorithms Unplugged. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-15328-0_8
        """

        """
        # adapted for steps (no loops!):

        1 Set angle counter to 0;
        2 Walk straight ahead;
        3 If not (wall hit) goto #2;
        4 Turn right;
        5 Follow the obstacle’s wall;
        6 If not (angle counter is 0) goto #5;
        7 If not (exit found) goto #2;
        8 End;
        """

        # define some helpful methods to avoid messy code and mistakes
        def setSolverStep(step: int) -> None:
            solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, step)

        def getSolverStep() -> int:
            return solver._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY][1]

        # Pledge-specific methods for helping with angle tracking
        def setPledgeAngle(angle: int) -> None:
            solver._state.solverSpecificVariables["pledgeAngle"] = (int, angle)

        def getPledgeAngle() -> int:
            try:
                angle = solver._state.solverSpecificVariables["pledgeAngle"][1]
                return angle
            except:
                # var not set, so set to 0
                setPledgeAngle(0)
                return 0

        step = getSolverStep()

        if step == 1:
            # set angle counter to 0
            setPledgeAngle(0)
            setSolverStep(2)

            commandHumanDescription = "Set angle to 0"
            commandType = MazeSolverCommandType.logic
            result = MazeSolverCommandResult(
                True, commandHumanDescription, solver._state
            )
        elif step == 2:
            result = solver._moveForward()
            setSolverStep(3)

            commandHumanDescription = "Move forward"
            commandType = MazeSolverCommandType.movement
        elif step == 3:
            # get the last command's result – and the last command has to be step #2 so we check if it hit a wall or not
            lastCommand = solver.getCompletedCommandsList()[-1]
            if lastCommand.commandResult is not None:
                if lastCommand.commandResult.success:
                    # if a wall was not hit
                    setSolverStep(2)
                else:
                    # a wall *was* hit
                    setSolverStep(4)

            commandHumanDescription = "Check for collision last time"
            commandType = MazeSolverCommandType.logic

            result = MazeSolverCommandResult(
                True, commandHumanDescription, solver._state
            )
        elif step == 4:
            result = solver._turn(RelativeDirection.right)
            setPledgeAngle(
                getPledgeAngle() + 90,
            )
            setSolverStep(5)

            commandHumanDescription = "Turn right"
            commandType = MazeSolverCommandType.movement
        elif step == 5:
            # follow the obstacle's wall
            oldDirection = solver._state.facingDirection.toDegrees()
            (_, result) = WallFollower.performAlgorithmOn(solver)
            newDirection = result.newState.facingDirection.toDegrees()

            directionDifference = newDirection - oldDirection
            setPledgeAngle(getPledgeAngle() + directionDifference)

            setSolverStep(6)

            commandHumanDescription = "Follow the obstacle's wall"
            commandType = MazeSolverCommandType.movement

            result = MazeSolverCommandResult(
                True, commandHumanDescription, solver._state
            )
        elif step == 6:
            if getPledgeAngle() != 0:
                setSolverStep(5)
            else:
                setSolverStep(7)

            commandHumanDescription = "Check angle counter is 0"
            commandType = MazeSolverCommandType.logic
            result = MazeSolverCommandResult(
                True, commandHumanDescription, solver._state
            )
        elif step == 7:
            if solver._state.currentCell != solver.endingPosition:
                # exit not found, goto #2
                setSolverStep(2)
            else:
                # finished!
                raise NotImplementedError("finished maze lol")

            commandHumanDescription = "Check solver is finished"
            commandType = MazeSolverCommandType.logic

            result = MazeSolverCommandResult(
                True, commandHumanDescription, solver._state
            )
        else:
            # we're in a weird state that shouldn't exist
            raise RuntimeError(
                f"Unknown Pledge maze solver error – undefined step {step}"
            )

        command = MazeSolverCommand(
            humanDescription=commandHumanDescription,
            commandType=commandType,
            commandResult=result,
        )

        # log the command and result
        logging.debug(command.humanDescription)
        if command.commandResult is not None:
            logging.debug(command.commandResult.humanDescription)

        return (command, result)


if __name__ == "__main__":
    # Test out the Pledge maze solver
    maze = RecursiveBacktracker(XY(10, 10)).generate()

    pledge = PledgeSolver(maze, XY(0, 0), XY(9, 9))

    FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
    LEVEL = 0
    logging.basicConfig(format=FORMAT, level=LEVEL)
    logging.getLogger().setLevel(LEVEL)
    log = logging.getLogger()

    from time import sleep

    while True:
        result = pledge.advance()
        sleep(0.25)

        print(pledge.getCurrentState().currentCell)
        # if finished
        if result.newState.solverSpecificVariables[PLEDGESOLVERSTEP_KEY][1] == 11:
            break
