from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.maze_solver_state import MazeSolverState
from typing import List, Tuple
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolverProtocol


class WallFollower(MazeSolverProtocol):
    # List of commands issued
    __commands: List[Tuple[MazeSolverCommand, MazeSolverState]]

    # The current state of the Maze Solver
    __state: MazeSolverState

    # the history of states so the user can see the progress of the solver in more depth
    __state_history: List[MazeSolverState]

    # __algorithm: str

    def __init__(self, maze: Maze) -> None:
        raise NotImplementedError()

    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.
        """
        raise NotImplementedError()

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