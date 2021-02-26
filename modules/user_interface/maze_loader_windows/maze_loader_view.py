from modules.user_interface.maze_loader_windows.maze_generator_window import (
    MazeGeneratorWindow,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.file_handling.maze.maze_file_handler import MazeFileHandler
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6.QtCore import pyqtSlot
from typing import Any, List, Optional, Tuple
from PyQt6.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget
import logging


class MazeLoaderView(QWidget):
    __onMazeSpecificationChosen: pyqtSlot(MazeGenerationSpecification)
    __onMazeLoaded: pyqtSlot(MazeProtocol)
    __onLoadLastMazeChosen: pyqtSlot()

    def __init__(
        self,
        onLoadLastMazePressed: pyqtSlot(),
        onMazeLoaded: pyqtSlot(MazeProtocol),
        onMazeSpecificationChosen: pyqtSlot(MazeGenerationSpecification),
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The view used for prompting the user to load, generate or load last maze.
        """
        super(MazeLoaderView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("Load a Maze")

        self.__onLoadLastMazeChosen = onLoadLastMazePressed
        self.__onMazeLoaded = onMazeLoaded
        self.__onMazeSpecificationChosen = onMazeSpecificationChosen

        # create layout
        layout = QVBoxLayout()

        # add all the buttons to the layout
        for button in self.__getButtons():
            layout.addWidget(button)

        self.setLayout(layout)

    def __getButtons(
        self,
    ) -> List[QPushButton]:
        loadMazeButton = QPushButton("Load Maze…")
        loadMazeButton.clicked.connect(self.__onLoadMazeButtonPressed)  # type: ignore

        generateMazeButton = QPushButton("Generate Maze…")
        generateMazeButton.clicked.connect(self.__onGenerateMazeButtonPressed)  # type: ignore

        loadLastMazeButton = QPushButton("Load Last Maze")
        loadLastMazeButton.clicked.connect(self.__onLoadLastMazeChosen)  # type: ignore

        elements: List[QPushButton] = [
            loadMazeButton,
            generateMazeButton,
            loadLastMazeButton,
        ]

        return elements

    def __onLoadMazeButtonPressed(self) -> None:
        fileDialog = QFileDialog(self, "Open a maze file…")
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

        self.__onMazeLoaded(
            maze,  # type: ignore
        )

    def __onGenerateMazeButtonPressed(self) -> None:
        """
        Presents a "Generate Maze" window to the user and connects the result signal to `self.__mazeGenerateButtonPressedWithSpecification`.
        """
        self.__mazeGeneratorWindow = MazeGeneratorWindow(parent=self)
        self.__mazeGeneratorWindow.onMazeSpecChosen.connect(
            self.__onMazeSpecificationChosen
        )
        self.__mazeGeneratorWindow.show()

    def destroy(self, destroyWindow: bool, destroySubWindows: bool) -> None:
        if destroySubWindows:
            self.__mazeGeneratorWindow.destroy(True, destroySubWindows)
        return super().destroy(
            destroyWindow=destroyWindow, destroySubWindows=destroySubWindows
        )
