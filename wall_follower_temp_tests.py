import logging

from modules.maze_solvers.solvers.random_mouse import RandomMouse

from modules.maze_generation.recursive_backtracker import (
    RecursiveBacktracker,
)

# from modules.maze_solvers.solvers.random_mouse import RandomMouse
from modules.common_structures.xy import XY
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.INFO
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

rb = RecursiveBacktracker(XY(15, 5))
maze = rb.generate()

# maze = Maze(5, 5, walls=False)
wallFollower = WallFollower(maze, XY(0, 0))
randomMouse = RandomMouse(maze, XY(0, 0))

i = 0

print("GO")
while True:
    wallFollower.advance()
    wallFollowerCell = wallFollower.getCurrentState().currentCell

    randomMouse.advance()
    randomMouseCell = randomMouse.getCurrentState().currentCell

    print("Wall Follower\t" + str(wallFollowerCell.toTuple()))
    print("Random Mouse\t" + str(randomMouseCell.toTuple()))

=    i += 1
