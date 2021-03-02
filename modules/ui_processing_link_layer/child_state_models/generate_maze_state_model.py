from PyQt6.QtWidgets import QWidget
from modules.ui_processing_link_layer.ui_state_model import StateModel
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)


class GenerateMazeGroupStateModel(StateModel):
    __view: GenerateMazeGroupView

    def __init__(self, parent: QWidget) -> None:
        self.__view = GenerateMazeGroupView(parent)

    def showView(self) -> None:
        self.__view.show()
