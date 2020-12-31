from modules.common_structures.xy import XY
from modules.data_structures.maze.maze.maze import Maze
from modules.file_handling.maze.maze_file_handler import MazeFileHandler
import unittest


class TestMazeFileHandler(unittest.TestCase):
    def testMazeIsSaved(self):
        FILEPATH = "test_save.maze"

        fileHandler = MazeFileHandler(FILEPATH)
        maze = Maze(4, 4, True)

        with self.assertLogs(level="DEBUG"):
            fileHandler.save(maze)

    def testMazeIsLoadedCorrectly(self):
        FILEPATH = "test_save.maze"

        size = XY(13, 3)

        # save the maze
        fileHandler = MazeFileHandler(FILEPATH)
        fileHandler.save(Maze(size.x, size.y, False))

        # try to load the maze
        newMaze = fileHandler.load()
        self.assertEqual(newMaze.size, size)

    def testLoadNonExistentFileWithException(self):
        FILEPATH = "nonexistentfile"

        # try to load it
        fileHandler = MazeFileHandler(FILEPATH)
        with self.assertRaises(
            FileNotFoundError,
            msg=f"FileNotFoundError: File at {FILEPATH} is corrupt or does not exist.",
        ):
            _ = fileHandler.load()


if __name__ == "__main__":
    unittest.main()