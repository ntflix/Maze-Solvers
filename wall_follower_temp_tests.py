import logging
from modules.common_structures.xy import XY
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.ERROR
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

maze = Maze(12, 12, walls=False)
wf = WallFollower(maze, XY(0, 0))

timesAt00 = 0
lastCell = (-1, -1)

while True:
    wf.advance()
    cell = wf.getCurrentState().currentCell.toTuple()

    if cell == (0, 0):
        if lastCell != (0, 0):
            timesAt00 += 1
            print(timesAt00)

    lastCell = cell
