from typing import Protocol


class MazeSolverCommandResult(Protocol):
    humanDescription: str
    success: bool

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.humanDescription
