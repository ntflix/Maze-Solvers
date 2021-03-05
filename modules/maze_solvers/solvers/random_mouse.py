import logging
from typing import Tuple
from modules.data_structures.maze.maze_protocol import MazeProtocol
import random
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


class RandomMouse(MazeSolver):
    def __init__(
        self,
        maze: MazeProtocol,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        # init superclass
        super().__init__(maze, startingPosition, startingDirection)

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

        logging.info("Advancing the random mouse.")

        command, result = self.performAlgorithmOn(self)

        # add to command history
        self._saveCommandToHistory(command)

        logging.info(f"{command.humanDescription}: {result.humanDescription}")

        return result

    @staticmethod
    def performAlgorithmOn(
        solver: "MazeSolver",
    ) -> Tuple[MazeSolverCommand, MazeSolverCommandResult]:
        # choose random direction to go in
        # absolute direction is less expensive than relative
        movementDirection = random.choice(AbsoluteDirection.allCases())
        solver._turnAbsolute(movementDirection)
        forward = solver._moveForward()

        result = MazeSolverCommandResult(
            forward.success,
            f"Turned {movementDirection} and attempted to move forward",
            solver._state,
        )

        command = MazeSolverCommand(
            "Move randomly",
            MazeSolverCommandType.movement,
            result,
        )

        return (command, result)


if __name__ == "__main__":
    # Test out the random mouse maze solver
    from modules.data_structures.maze.maze import Maze

    maze = Maze(10, 10, False)
    rm = RandomMouse(maze, XY(0, 0))

    FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
    LEVEL = 0
    logging.basicConfig(format=FORMAT, level=LEVEL)
    logging.getLogger().setLevel(LEVEL)
    log = logging.getLogger()

    while True:
        rm.advance()
        print(rm.getCurrentState().currentCell)
