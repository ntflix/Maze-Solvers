import logging
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.maze_solver_state import MazeSolverState
from typing import List, Tuple
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver


class WallFollower(MazeSolver):
    def __init__(self, maze: Maze) -> None:
        # init superclass
        super().__init__(maze)
        logging.debug(f"Initialized Wall Follower maze solver with maze {maze}")

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.

        The algorithm for this is as follows:
        ```
        1   GO forward
        2       Collision?
        3           YES:
        4               UNTIL (no obstacle in front):
        5                   TURN right
        6               GO forward
        7               TURN left
        8                   Collision?
        9                       YES:
        10                          GOTO #4
        11                      NO:
        12                          GOTO #7
        13          NO:
        14              GOTO #1
        15      TURN left
        ```
        """
        logging.debug("Attempting to advance the wall follower")

    def getCompletedCommandsWithNewStateList(
        self,
    ) -> List[Tuple[MazeSolverCommand, MazeSolverState]]:
        # commands are separate from state and
        # the state should never be modified
        # because of the command list.
        # commands are solely for feedback to user.

        # and the history of MazeSolverStates so the user can see the progress of the solver in more depth
        raise NotImplementedError()

    def getCurrentState(self) -> MazeSolverState:
        # the current state of the maze solver
        raise NotImplementedError()