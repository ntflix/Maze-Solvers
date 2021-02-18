from modules.common_structures.xy import XY


class MazeSolverSpecification:
    startPosition: XY
    endPosition: XY

    def __init__(
        self,
        startPosition: XY,
        endPosition: XY,
    ) -> None:
        self.startPosition = startPosition
        self.endPosition = endPosition