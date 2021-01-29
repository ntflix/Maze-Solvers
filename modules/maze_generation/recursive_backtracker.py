from modules.maze_generation.maze_generator import MazeGenerator
from modules.data_structures.stack.stack import Stack
from random import choice as randomChoice
from typing import Callable, List, Optional
from modules.common_structures.xy import XY
from modules.data_structures.maze.maze import Maze


class RecursiveBacktracker(MazeGenerator):
    """Recursive Backtracker maze generation algorithm implementation.

    |    Here’s the mile-high view of recursive backtracking:
    |
    |    • Choose a starting point in the field.
    |    • Randomly choose a wall at that point and carve a passage through to the adjacent cell, but only if the adjacent cell has not been visited yet.
    |           This becomes the new current cell.
    |    • If all adjacent cells have been visited, back up to the last cell that has uncarved walls and repeat.
    |    • The algorithm ends when the process has backed all the way up to the starting point.
    > Source - http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
    """

    __maze: Maze
    __visitedOrNotCells: List[bool]  # the cell index is the position in the list
    __size: XY
    # the stack of positions
    __positionsStack: Stack[int]

    def __init__(self, size: XY) -> None:
        self.__size = size
        # initialize a Maze full of walls
        self.__maze = Maze(self.__size.x, self.__size.y, walls=True)

        # get the last cell index of the maze, so we can initialise __visitedOrNotCells to a list of False (nothing visited yet)
        lastIndex = self.__maze.getIndexFromCoordinates(
            XY(self.__size.x - 1, self.__size.y - 1)
        )
        # init __visitedOrNotCells to a list of False with the length of the max index of cells
        self.__visitedOrNotCells = [False] * (lastIndex + 1)

    def generate(self) -> Maze:
        # start our maze generator in the top left of the maze
        start = XY(0, 0)

        # init positionsStack to a new empty stack of type int
        self.__positionsStack = Stack[int]()

        # Convert the `start` position to the same cell's index in the maze, and push to the positions stack
        self.__positionsStack.push(
            # get the index of the `start` posotion
            self.__maze.getIndexFromCoordinates(start)
        )

        # set the starting cell as visited
        self.__visitedOrNotCells[self.__positionsStack.peek()] = True

        # while the positions stack is not empty, so we automatically exit the loop when visited all cells and back at start
        while not self.__positionsStack.isEmpty():
            randomCellChoice: Optional[int] = None
            # this loop tries to find a random cell to visit out of the unvisited neighbours of the current cell
            while randomCellChoice is None:
                # if we've ran out of positions to backtrack to, and therefore made the entire maze
                if self.__positionsStack.isEmpty():
                    break

                # get a list of unvisited adjacent cells
                neighbourCells = self.__maze.getNeighboursOfCell(
                    # get the current position by peeking the stack.
                    # don't pop because we want the item to remain on the stack,
                    # so we can backtrach through it.
                    self.__positionsStack.peek()
                )

                # Filter the neighbourCells by whether they've been visited or not
                # create a lambda to return whether or not a cell at index has been visited, but return the inverse because we are _filtering_ the cells!
                checkIsVisited: Callable[
                    [int], bool
                ] = lambda cellIndex: not self.__visitedOrNotCells[cellIndex]
                # and filter the neighbourCells by this lambda, and put it into the list variable `unvisitedWalls`
                unvisitedWalls = list(filter(checkIsVisited, neighbourCells))

                # check that there are unvisited walls
                if len(unvisitedWalls) > 0:
                    # choose a random wall
                    randomCellChoice = randomChoice(unvisitedWalls)
                    # set the next cell to visited
                    self.__visitedOrNotCells[randomCellChoice] = True
                else:
                    # all the cells here have been visited
                    # so back up to the last cell, by popping the positionsStack
                    self.__positionsStack.pop()

            # if the cell hasn't been chosen, and therefore we've explored the whole maze
            if randomCellChoice is None:
                # break so we can return the completed maze
                break

            # carve a passage through to the adjacent cell
            self.__maze.removeWallBetween(
                cellAIndex=self.__positionsStack.peek(),
                cellBIndex=randomCellChoice,
            )
            # push the choice to the positionsStack so it is our next one
            self.__positionsStack.push(randomCellChoice)

        return self.__maze
