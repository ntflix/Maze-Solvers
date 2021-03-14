from modules.maze_solvers.maze_solver_state import MazeSolverState


class MazeSolverCommandResult:
    success: bool
    humanDescription: str
    newState: MazeSolverState

    def __init__(
        self,
        success: bool,
        humanDescription: str,
        state: MazeSolverState,
    ) -> None:
        self.success = success
        self.humanDescription = humanDescription
        self.newState = state

    def __repr__(self) -> str:
        return self.humanDescription

    @staticmethod
    def finished(state: MazeSolverState) -> "MazeSolverCommandResult":
        return MazeSolverCommandResult(True, "Finished", state)