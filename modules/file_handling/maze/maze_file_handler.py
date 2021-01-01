import logging
from modules.file_handling.file_persistence import FilePersistence
from modules.data_structures.maze.maze_protocol import MazeProtocol
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
        # try to load file
        loaded = self.__persistence.load(key=self.__key)

        if isinstance(loaded, MazeProtocol):  # type: ignore
            # type checker says, "Unnecessary isinstance call; "MazeProtocol" is always an instance of "MazeProtocol"
            # I mean yes, that's what I'm checking, because Python does not enforce strict types. Thanks anyway Pylance.
            return loaded
        else:
            errorMessage = (
                f"Imported `maze` object from file {self.__path}"
                " does not conform to `MazeProtocol` and"
                " thus cannot be used as a maze object."
            )
            # log the error in this class's error channel
            logging.error(errorMessage)
            # imported maze does not conform to MazeProtocol
            raise RuntimeError(errorMessage)

    def save(self, object: MazeProtocol) -> None:
        return self.__persistence.save(object, key=self.__key)