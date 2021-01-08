from enum import Enum


class RelativeDirection(Enum):
    # used to keep track of the directions relative to an agent in a maze
    forward = (0, 1)
    right = (1, 0)
    backward = (0, -1)
    left = (-1, 0)