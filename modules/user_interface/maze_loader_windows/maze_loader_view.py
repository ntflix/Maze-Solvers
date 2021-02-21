from modules.file_handling.maze.maze_file_handler import MazeFileHandler
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.common_structures.xy import XY
from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
from PyQt6 import QtCore
from modules.user_interface.maze_loader_windows.maze_generator_window import (
    MazeGeneratorWindow,
)
from typing import Any, List, Optional, Tuple
from PyQt6.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget
import logging


class MazeLoaderView(QWidget):
    gotMaze = QtCore.pyqtSignal(MazeProtocol)

    def __init__(
        self,
        lastSaveMazePath: str,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The view used for prompting the user to load, generate or load last maze.
        """
        super(MazeLoaderView, self).__init__(parent=parent, *args, **kwargs)
        self.__parent = parent

        layout = QVBoxLayout()
        for button in self.__getButtons():
            layout.addWidget(button)

        self.setLayout(layout)

    def __getButtons(self) -> List[QPushButton]:
        loadMazeButton = QPushButton("Load Maze…")
        loadMazeButton.clicked.connect(self.__onLoadMazeButtonPressed)  # type: ignore

        generateMazeButton = QPushButton("Generate Maze…")
        generateMazeButton.clicked.connect(self.__onGenerateMazeButtonPressed)  # type: ignore

        loadLastConfigButton = QPushButton("Load Last Maze")
        loadLastConfigButton.clicked.connect(self.__onLoadLastMazeButtonPressed)  # type: ignore

        elements: List[QPushButton] = [
            loadMazeButton,
            generateMazeButton,
            loadLastConfigButton,
        ]

        return elements

    def __onLoadMazeButtonPressed(self) -> None:
        fileDialog = QFileDialog(self.__parent, "Open a maze file…")
        filesFilter = "Maze files (*.maze, *.db)"
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        filePath: str = ""
        maze: MazeProtocol
        mazeIsValid = False

        while not mazeIsValid:
            filePath = fileDialog.getOpenFileName(filter=filesFilter)[0]
            fileHandler = MazeFileHandler(filePath)
            try:
                maze = fileHandler.load()
                mazeIsValid = True
            except FileNotFoundError as noFileError:
                logging.error(f"Maze file does not exist: {noFileError}")
                raise FileNotFoundError()
            except RuntimeError as invalidFileError:
                logging.error(f"Invalid maze file: {invalidFileError}")
                raise FileNotFoundError()
        
        self.gotMaze.emit(maze) # type: ignore

    def __onGenerateMazeButtonPressed(self) -> None:
        mazeGeneratorWindow = MazeGeneratorWindow(self)
        mazeGeneratorWindow.gotMaze.connect(self.gotMaze)
        mazeGeneratorWindow.show()

    def __onLoadLastMazeButtonPressed(self) -> None:
        print("load button pressed")
        mazeGenerator = RecursiveBacktracker(XY(10, 10))
        maze = mazeGenerator.generate()
        self.gotMaze.emit(maze)
