import logging
from modules.data_structures.maze.maze import Maze

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

rb = RecursiveBacktracker(XY(15, 5))
maze = rb.generate(XY(0, 0))

# maze = Maze(5, 5, walls=False)
solver = WallFollower(maze, XY(0, 0))

i = 0
lastCell = XY(-1, -1)

print("GO")
while True:
    solver.advance()
    cell = solver.getCurrentState().currentCell

    print(cell.toTuple())

    i += 1
    if lastCell != cell:
        assert True

    lastCell = cell

commands = solver.getCompletedCommandsList()
assert ()
