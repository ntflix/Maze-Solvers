from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.maze_solver_state import MazeSolverState
from typing import List
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolverProtocol


class WallFollower(MazeSolverProtocol):
    # List of commands issued
    commands: List[MazeSolverCommand]

    # The current state of the Maze Solver
    state: MazeSolverState

    # the history of states so the user can see the progress of the solver in more depth
    state_history: List[MazeSolverState]

    # __algorithm: str

    def __init__(self, maze: Maze) -> None:
        raise NotImplementedError()

    def advance(self) -> MazeSolverCommandResult:
        raise NotImplementedError()
