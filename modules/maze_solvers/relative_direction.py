from enum import Enum
from typing import Tuple


class RelativeDirection(Enum):
    # used to keep track of the directions relative to an agent in a maze
    forward = (0, 1)
    right = (1, 0)
    backward = (0, -1)
    left = (-1, 0)

    def toAllParts(self) -> Tuple[int, int, int, int]:
        # forward, right, backward, left
        result = [0, 0, 0, 0]

        if self.value[0] == -1:
            # left
            result[3] = 1
        elif self.value[0] == 1:
            # right
            result[1] = 1
        elif self.value[1] == -1:
            # backward
            result[2] = 1
        elif self.value[1] == 1:
            # forward
            result[0] = 1

        return tuple(result)