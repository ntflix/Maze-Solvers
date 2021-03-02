from typing import Protocol
from PyQt6.QtWidgets import QWidget
from modules.user_interface.main_window import MazeSolverUI


class UIStateModel:
    __ui: MazeSolverUI

    def __init__(self, ui: MazeSolverUI) -> None:
        self.__ui = ui

    def startApplication(self) -> int:
        return self.__ui.exec()


class StateModel(Protocol):
    def __init__(self, parent: QWidget) -> None:
        raise NotImplementedError("Tried calling initializer method on Protocol class")

    def getAsParent(self) -> QWidget:
        raise NotImplementedError("Tried calling `getAsParent` on Protocol class")

    def showView(self) -> None:
        raise NotImplementedError("Tried calling `showView` on Protocol class")
