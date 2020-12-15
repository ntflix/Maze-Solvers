from typing import Iterator


class XY:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"