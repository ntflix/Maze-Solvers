from modules.common_structures.xy import XY


class MazeGenerationSpecification:
    size: XY
    simplyConnected: bool

    def __init__(
        self,
        size: XY,
        simplyConnected: bool,
    ) -> None:
        self.size = size
        self.simplyConnected = simplyConnected