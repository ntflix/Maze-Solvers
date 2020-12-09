from typing import Protocol


class MazeSolverProtocol(Protocol):
    def __init__(self) -> None:
        pass

    def advance(self):
