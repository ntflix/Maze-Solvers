from modules.common_structures.xy import XY
from modules.data_structures.maze.maze.maze import Maze
from modules.file_handling.maze.maze_file_handler import MazeFileHandler
import unittest


class TestMazeFileHandler(unittest.TestCase):
    FILE_PATH_PREFIX = "_unittest/file_handling/maze/sample_data/"

    def testMazeIsSaved(self):
        FILEPATH = self.FILE_PATH_PREFIX + "test_save.maze"

        fileHandler = MazeFileHandler(FILEPATH)
        maze = Maze(4, 4, True)

        with self.assertLogs(level="DEBUG"):
            fileHandler.save(maze)

    def testMazeIsLoadedCorrectly(self):
        FILEPATH = self.FILE_PATH_PREFIX + "test_save.maze"

        size = XY(13, 3)

        # save the maze
        fileHandler = MazeFileHandler(FILEPATH)
        fileHandler.save(Maze(size.x, size.y, False))

        # try to load the maze
        newMaze = fileHandler.load()
        self.assertEqual(newMaze.size, size)

    def testLoadNonExistentFileWithException(self):
        FILEPATH = self.FILE_PATH_PREFIX + "nonexistentfile"

        # try to load it
        fileHandler = MazeFileHandler(FILEPATH)
        with self.assertRaises(
            FileNotFoundError,
            msg=f"FileNotFoundError: File at {FILEPATH} is corrupt or does not exist.",
        ):
            _ = fileHandler.load()


if __name__ == "__main__":
    unittest.main()
