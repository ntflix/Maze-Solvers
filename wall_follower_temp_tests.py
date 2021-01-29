import logging

# from modules.maze_solvers.solvers.random_mouse import RandomMouse

from modules.maze_generation.algorithms.recursive_backtracker import (
    RecursiveBacktracker,
)

# from modules.maze_solvers.solvers.random_mouse import RandomMouse
from modules.common_structures.xy import XY
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.INFO
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

maze = RecursiveBacktracker(XY(10, 10)).generate(XY(0, 0))

# maze = Maze(50, 5, walls=False)
solver = WallFollower(maze, XY(0, 0))

i = 0

print("GO")
while True:
    solver.advance()
    cell = solver.getCurrentState().currentCell.toTuple()

    print(cell)

    i += 1
    if i > 20:
        break

commands = solver.getCompletedCommandsList()
assert ()
