from enum import Enum


class MazeSolverCommandType(Enum):
    # the type of command for a maze solver agent to execute
    detection = "Detection"
    movement = "Movement"
