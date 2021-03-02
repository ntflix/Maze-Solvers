from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.file_handling.maze.maze_file_handler import MazeFileHandler
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from typing import Protocol
from PyQt6.QtWidgets import QWidget
from modules.user_interface.main_window import MazeSolverUI
import logging


class UIStateModel:
    __ui: MazeSolverUI

    def __init__(self) -> None:
        self.__initUI()

    def __initUI(self) -> None:
        self.__ui = MazeSolverUI(
            onLoadLastMazePressed=self.__onLoadLastMazePressed,
            onMazeFilePathChosen=self.__onMazeFilePathChosen,
            onPlayButtonPressed=self.__onPlayButtonPressed,
            onPauseButtonPressed=self.__onPauseButtonPressed,
            onStepButtonPressed=self.__onStepButtonPressed,
            onRestartButtonPressed=self.__onRestartButtonPressed,
            onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
            onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
            onAgentVarsButtonPressed=self.__onAgentVarsButtonPressed,
            onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
        )

    def __onMazeInstantiated(self, maze: MazeProtocol) -> None:
        print(maze)

    def __onLoadLastMazePressed(self) -> None:
        print("__onLoadLastMazePressed")

    def __onMazeFilePathChosen(self, filePath: str) -> None:
        maze: MazeProtocol
        mazeIsValid = False

        while not mazeIsValid:
            fileHandler = MazeFileHandler(filePath)
            try:
                maze = fileHandler.load()
            except FileNotFoundError as noFileError:
                logging.error(f"Maze file does not exist: {noFileError}")
                raise FileNotFoundError()
            except RuntimeError as invalidFileError:
                logging.error(f"Invalid maze file: {invalidFileError}")
                raise FileNotFoundError()
            else:
                logging.debug(f"Maze loaded from `{filePath}` successfully.")
                print("__onMazeLoaded")
                self.__onMazeInstantiated(maze)
                break

    def __onPlayButtonPressed(self) -> None:
        print("__onPlayButtonPressed")

    def __onPauseButtonPressed(self) -> None:
        print("__onPauseButtonPressed")

    def __onStepButtonPressed(self) -> None:
        print("__onStepButtonPressed")

    def __onRestartButtonPressed(self) -> None:
        print("__onRestartButtonPressed")

    def __onSpeedControlValueChanged(self, newValue: int) -> None:
        print("__onSpeedControlValueChanged")

    def __onOpenLogButtonPressed(self) -> None:
        print("__onOpenLogButtonPressed")

    def __onAgentVarsButtonPressed(self) -> None:
        print("__onAgentVarsButtonPressed")

    def __onGenerateMazeButtonPressed(
        self,
        mazeSpecification: MazeGenerationSpecification,
    ) -> None:
        logging.debug(
            f"Generate Maze button pressed with maze specification: {mazeSpecification}"
        )
        print("__onGenerateMazeButtonPressed", mazeSpecification)

    def startApplication(self) -> int:
        return self.__ui.exec()


class UIWidgetState(Protocol):
    def __init__(self, parent: QWidget) -> None:
        raise NotImplementedError("Tried calling initializer method on Protocol class")

    def getAsParent(self) -> QWidget:
        raise NotImplementedError("Tried calling `getAsParent` on Protocol class")

    def showView(self) -> None:
        raise NotImplementedError("Tried calling `showView` on Protocol class")
