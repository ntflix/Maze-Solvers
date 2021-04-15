from typing import Iterator, Tuple


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

    def __eq__(self, o: object) -> bool:
        if type(o) == XY:
            return (self.x, self.y) == (o.x, o.y)  # type: ignore
        else:
            return False

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    def __hash__(self) -> int:
        return hash(self.toTuple())

    def toTuple(self) -> Tuple[int, int]:
        return (self.x, self.y)
