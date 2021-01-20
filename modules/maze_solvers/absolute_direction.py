from enum import Enum
from modules.maze_solvers.relative_direction import RelativeDirection


class AbsoluteDirection(Enum):
    # used to keep track of absolute directions
    north = (0, 1)
    east = (1, 0)
    south = (0, -1)
    west = (-1, 0)

    def toDegrees(self) -> int:
        degrees = {
            AbsoluteDirection.north: 0,
            AbsoluteDirection.east: 90,
            AbsoluteDirection.south: 180,
            AbsoluteDirection.west: 270,
        }

        return degrees[self]

    @staticmethod
    def fromDegrees(degrees: int) -> "AbsoluteDirection":
        directions = {
            0: AbsoluteDirection.north,
            90: AbsoluteDirection.east,
            180: AbsoluteDirection.south,
            270: AbsoluteDirection.west,
        }

        return directions[degrees]

    @staticmethod
    def fromRelativeDirection(
        relativeDirection: RelativeDirection, facingDirection: "AbsoluteDirection"
    ) -> "AbsoluteDirection":
        """Calculate an absolute direction from a relative direction and absolute direction.

        Returns:
            AbsoluteDirection: The calculated direction.
        """
        newDirectionDegrees = (
            facingDirection.toDegrees() + relativeDirection.toDegrees()
        ) % 360
        newDirection = AbsoluteDirection.fromDegrees(newDirectionDegrees)

        return newDirection
