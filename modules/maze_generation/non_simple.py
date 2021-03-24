from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
from modules.data_structures.maze.maze import Maze
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.maze_generation.maze_generator import MazeGenerator
from modules.common_structures.xy import XY
import random


class NonSimple(MazeGenerator):
    """Non-Simple maze generation algorithm hijacking the capabilities of the Recursive Backtracker implementation.

    Process:
    • Generate a maze with recursive backtracker
    • Delete random walls
    • Done!
    """

    __maze: MazeProtocol
    __size: XY

    def __init__(self, size: XY) -> None:
        # check size is valid
        self._testSizeIsValidWithException(size)

        self.__size = size
        # initialize a Maze full of walls
        self.__maze = Maze(self.__size.x, self.__size.y, walls=True)

    def generate(self) -> MazeProtocol:
        # generate a simply-connected maze with the recursive backtracker
        self.__maze = RecursiveBacktracker(self.__size).generate()

        # the probability of removing each wall
        probabilityOfRemoveWall = 0.2

        for x in range(0, self.__size.x):
            for y in range(0, self.__size.y):
                currentPosition = XY(x, y)
                currentIndex = self.__maze.getIndexFromCoordinates(currentPosition)

                connectionsWithoutWalls = set(
                    self.__maze.getConnectionsOfCellAtIndex(currentIndex)
                )
                allNeighbours = set(self.__maze.getNeighboursOfCell(currentIndex))
                walledNeighbours = allNeighbours - connectionsWithoutWalls

                for neighbour in walledNeighbours:
                    # get a true or false based off the probability of before
                    shouldDeleteThisWall = random.random() < probabilityOfRemoveWall
                    if shouldDeleteThisWall:
                        # delete the wall between the two cells
                        self.__maze.removeWallBetween(
                            cellAIndex=currentIndex,
                            cellBIndex=neighbour,
                        )

        return self.__maze
