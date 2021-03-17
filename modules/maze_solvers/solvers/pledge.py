import logging
from modules.maze_solvers.solvers.wall_follower import WallFollower
from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
from typing import Tuple
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.maze_solvers.commands.commands.maze_solver_command_type_enum import (
    MazeSolverCommandType,
)
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

        # init Pledge vars
        # start in step 1
        self._state.solverSpecificVariables[PLEDGESOLVERSTEP_KEY] = (int, 1)
        # start with angle 0
        self._state.solverSpecificVariables["pledgeAngle"] = (int, 0)

        self._state.solverSpecificVariables["lastSuccessfulForwardMove"] = (
            bool,
            True,
        )

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

        """
        The Pledge algorithm, designed to circumvent obstacles, requires an arbitrarily chosen direction to go toward.
        When an obstacle is met, one hand (say the right hand) is kept along the obstacle while the angles turned are counted.
        When the solver is facing the original direction again, and the angular sum of the turns made is 0, the solver leaves the obstacle and continues moving in its original direction.
        """
        step = getSolverStep()
        CHOSEN_DIRECTION = AbsoluteDirection.north

        if step == 1:
            commandHumanDescription = "Turn to face chosen direction and move forward"
            commandType = MazeSolverCommandType.movement

            result = MazeSolverCommandResult(
                True, f"Go {CHOSEN_DIRECTION}", solver._state
            )
            if solver._state.facingDirection != CHOSEN_DIRECTION:
                solver._turnAbsolute(CHOSEN_DIRECTION)
            result = solver._moveForward()
            if result.success is False:
                # if we've hit a wall, go to step 2, else just stay on step 1 and keep going
                setSolverStep(2)

        elif step == 2:
            result = MazeSolverCommandResult(True, "Followed wall", solver._state)

            oldDirection = solver._state.facingDirection

            (command, result) = WallFollower.performAlgorithmOn(solver)
            commandHumanDescription = command.humanDescription
            commandType = command.commandType

            newDirection = result.newState.facingDirection

            changeInDirection = newDirection.toDegrees() - oldDirection.toDegrees()
            # if we've moved from 270 to 0 degrees suddenly, something's up, so check it and fix the calculated angle:
            if oldDirection == AbsoluteDirection.west:
                if newDirection == AbsoluteDirection.north:
                    # moved from 270 to 0, meaning a changeInDirection of -270 (invalid)
                    changeInDirection = 90
            elif oldDirection == AbsoluteDirection.north:
                if newDirection == AbsoluteDirection.west:
                    # moved from 0 to 270, meaning a changeInDirection of 270 (invalid)
                    changeInDirection = -90

            setPledgeAngle(getPledgeAngle() + changeInDirection)

            setSolverStep(3)

        elif step == 3:
            commandHumanDescription = (
                "Check facing direction and Pledge angle to determine next step"
            )
            commandType = MazeSolverCommandType.logic

            result = MazeSolverCommandResult(
                True, "Checked solver facing direction and Pledge angle", solver._state
            )
            # set solver step to 2 here, in case next steps are not satisfied
            setSolverStep(2)
            if solver._state.facingDirection == CHOSEN_DIRECTION:
                if getPledgeAngle() == 0:
                    setSolverStep(1)

        else:
            logging.error(
                f"Something unexpected happened: the Pledge solver is in an unknown step {step}. This should be impossible as there are no code routes to set the step to this value."
            )
            raise RuntimeError(
                f"Pledge solver is in unknown step {step}! Last command issued was {solver.getCompletedCommandsList()[-1]}."
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
    maze = RecursiveBacktracker(XY(4, 5)).generate()

    pledge = PledgeSolver(maze, XY(0, 0), XY(3, 4))

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

        if result.newState.solverSpecificVariables[PLEDGESOLVERSTEP_KEY][1] == 7:
            print(pledge.getCurrentState().currentCell)
        # if finished
        # if "finished" in result:
        # pass
        # break
