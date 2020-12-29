from modules.data_structures.maze.maze.maze import Maze
from modules.data_structures.maze.maze.maze_protocol import MazeProtocol
from modules.file_handling.file_handler import FileHandler


class MazeFileHandler(FileHandler[MazeProtocol]):
    #  A file handler for MazeProtocol objects

    def __init__(self, path: str) -> None:
        pass

    def load(self) -> MazeProtocol:
        self.__close()
        return Maze(4, 4)
        pass

    def save(self, object: MazeProtocol) -> None:
        self.__close()
        pass

    def __close(self) -> None:
        raise NotImplementedError()
        pass