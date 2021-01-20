import logging
from modules.maze_solvers.solvers.random_mouse import RandomMouse
from modules.common_structures.xy import XY
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.INFO
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

maze = Maze(37, 7, walls=False)
solver = RandomMouse(maze, XY(0, 0))

timesAt00 = 0
lastCell = (-1, -1)
i = 0

print("GO")
while True:
    solver.advance()
    cell = solver.getCurrentState().currentCell.toTuple()
    # if cell == (0, 0):
    #     if lastCell != (0, 0):
    #         timesAt00 += 1
    #         print(timesAt00)

    print(cell)
    # time.sleep(0.5)

    # lastCell = cell
    i += 1
    if i > 200:
        break

commands = solver.getCompletedCommandsWithNewStateList()
assert ()
