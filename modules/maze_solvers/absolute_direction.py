from enum import Enum


class AbsoluteDirection(Enum):
    # used to keep track of absolute directions
    north = (0, 1)
    east = (1, 0)
    south = (0, -1)
    west = (-1, 0)