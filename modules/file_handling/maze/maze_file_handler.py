from modules.file_handling.file_persistence import FilePersistence
from modules.data_structures.maze.maze.maze_protocol import MazeProtocol
from modules.file_handling.file_handler import FileHandler


class MazeFileHandler(FileHandler[MazeProtocol]):
    """A file handler for MazeProtocol objects"""

    __path: str  # shelve db file path
    __key = "maze"  # shelve object key
    __persistence: FilePersistence[MazeProtocol]

    def __init__(self, path: str) -> None:
        """Initialize a MazeFileHandler object with a given path.

        Args:
            path (str): The path of the file to load/save from.
        """
        self.__path = path
        self.__persistence = FilePersistence[MazeProtocol](self.__path)
        pass

    def load(self) -> MazeProtocol:
        return self.__persistence.load(key=self.__key)

    def save(self, object: MazeProtocol) -> None:
        return self.__persistence.save(object, key=self.__key)