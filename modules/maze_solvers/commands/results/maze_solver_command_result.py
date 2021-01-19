from modules.maze_solvers.maze_solver_state import MazeSolverState


class MazeSolverCommandResult:
    humanDescription: str
    newState: MazeSolverState

    def __init__(
        self,
        humanDescription: str,
        state: MazeSolverState,
    ) -> None:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self.humanDescription
