from modules.maze_solvers.commands.protocols.maze_solver_command_result import (
    MazeSolverCommandResult,
)


class MovementCommandResult(MazeSolverCommandResult):
    humanDescription: str

    def __init__(self, description: str):
        self.humanDescription = description
