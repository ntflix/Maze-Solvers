from typing import Protocol


class MazeSolverCommandResult(Protocol):
    humanDescription: str

    def __init__(self, description: str) -> None:
        pass

    def __repr__(self) -> str:
        return self.humanDescription
