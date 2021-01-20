import logging
from modules.maze_solvers.maze_solver_state import MazeSolverState
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)


class DetectionCommandResult(MazeSolverCommandResult):
    obstacleExists: bool

    def __init__(
        self,
        success: bool,
        obstacleExists: bool,
        humanDescription: str,
        state: MazeSolverState,
    ) -> None:
        self.success = success
        self.obstacleExists = obstacleExists
        self.humanDescription = humanDescription
        self.newState = state

        logging.debug(
            f"Initialised MazeSolverCommandResult with parameters ({success, humanDescription, state})"
        )