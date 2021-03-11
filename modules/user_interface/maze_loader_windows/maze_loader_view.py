from modules.user_interface.maze_loader_windows.maze_generator_window import (
    MazeGeneratorWindow,
)
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from typing import Any, Callable, List, Optional, Tuple
from PyQt6.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget


class MazeLoaderView(QWidget):
    __onMazeSpecificationChosen: Callable[[MazeGenerationSpecification], None]
    __onMazeFilePathChosen: Callable[[str], None]
    __onLoadLastMazeChosen: Callable[[], None]
    __mazeGeneratorWindow: MazeGeneratorWindow
    __hasMazeGeneratorSubwindow: bool = False

    def __init__(
        self,
        onLoadLastMazePressed: Callable[[], None],
        onMazeLoadedFromPath: Callable[[str], None],
        onMazeSpecificationChosen: Callable[[MazeGenerationSpecification], None],
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
        self.__onMazeFilePathChosen = onMazeLoadedFromPath
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
        loadMazeButton.pressed = self.__onLoadMazeButtonPressed

        generateMazeButton = QPushButton("Generate Maze…")
        generateMazeButton.pressed = self.__onGenerateMazeButtonPressed

        loadLastMazeButton = QPushButton("Load Last Maze")
        loadLastMazeButton.pressed = self.__onLoadLastMazeChosen

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

        filePath = fileDialog.getOpenFileName(filter=filesFilter)[0]
        self.__onMazeFilePathChosen(filePath)

    def __onGenerateMazeButtonPressed(self) -> None:
        """
        Presents a "Generate Maze" window to the user and connects the result signal to `self.__mazeGenerateButtonPressedWithSpecification`.
        """
        self.__hasMazeGeneratorSubwindow = True
        self.__mazeGeneratorWindow = MazeGeneratorWindow(parent=self)
        self.__mazeGeneratorWindow.onMazeSpecChosen.connect(
            self.__onMazeSpecificationChosen
        )
        self.__mazeGeneratorWindow.show()

    def destroy(self, destroyWindow: bool, destroySubWindows: bool) -> None:
        if self.__hasMazeGeneratorSubwindow:
            if destroySubWindows:
                self.__mazeGeneratorWindow.destroy(True, destroySubWindows)
            return super().destroy(
                destroyWindow=destroyWindow, destroySubWindows=destroySubWindows
            )
