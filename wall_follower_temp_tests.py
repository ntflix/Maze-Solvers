import logging
from modules.maze_solvers.solvers.random_mouse import RandomMouse
from modules.common_structures.xy import XY
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.INFO
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

maze = Maze(357, 72, walls=False)
solver = RandomMouse(maze, XY(0, 0))

i = 0

print("GO")
while True:
    solver.advance()
    cell = solver.getCurrentState().currentCell.toTuple()

    print(cell)

    i += 1
    if i > 2000:
        break

commands = solver.getCompletedCommandsList()
assert ()
