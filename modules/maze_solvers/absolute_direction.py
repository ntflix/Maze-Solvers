from enum import Enum
from typing import Tuple
from modules.maze_solvers.relative_direction import RelativeDirection


class AbsoluteDirection(Enum):
    # used to keep track of absolute directions
    north = (0, 1)
    east = (1, 0)
    south = (0, -1)
    west = (-1, 0)

    @staticmethod
    def fromRelativeDirection(
        relativeDirection: RelativeDirection, facingDirection: "AbsoluteDirection"
    ) -> "AbsoluteDirection":
        print(str(facingDirection.toAllParts()) + f"\t{facingDirection}")
        print(str(relativeDirection.toAllParts()) + f"\t{relativeDirection}")
        print()
        raise NotImplementedError()

    def toAllParts(self) -> Tuple[int, int, int, int]:
        # north, east, south, west
        result = [0, 0, 0, 0]

        if self.value[0] == -1:
            # west
            result[3] = 1
        elif self.value[0] == 1:
            # east
            result[1] = 1
        elif self.value[1] == -1:
            # south
            result[2] = 1
        elif self.value[1] == 1:
            # north
            result[0] = 1

        return tuple(result)


for absoluteDirection in [
    AbsoluteDirection.north,
    AbsoluteDirection.east,
    AbsoluteDirection.south,
    AbsoluteDirection.west,
]:
    for relativeDirection in [
        RelativeDirection.forward,
        RelativeDirection.right,
        RelativeDirection.backward,
        RelativeDirection.left,
    ]:
        AbsoluteDirection.fromRelativeDirection(relativeDirection, absoluteDirection)
