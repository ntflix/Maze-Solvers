from enum import Enum


class RelativeDirection(Enum):
    # used to keep track of the directions relative to an agent in a maze
    forward = 0
    right = 1
    backward = 2
    left = 3