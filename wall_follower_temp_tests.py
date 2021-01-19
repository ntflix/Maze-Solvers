import logging
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.solvers.wall_follower import WallFollower


FORMAT = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
LEVEL = logging.DEBUG
logging.basicConfig(format=FORMAT, level=LEVEL)
log = logging.getLogger()

maze = Maze(10, 10)
wallFollower = WallFollower(maze)

wallFollower.advance()
