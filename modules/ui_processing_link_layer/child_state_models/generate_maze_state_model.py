from modules.user_interface.ui_translation.maze_generation_specification import MazeGenerationSpecification
from PyQt6.QtWidgets import QWidget
from modules.ui_processing_link_layer.ui_state_model import UIWidgetState
from modules.user_interface.maze_view.controls.generate_maze_group_view import (
    GenerateMazeGroupView,
)


class GenerateMazeGroupState(UIWidgetState):
    __view: GenerateMazeGroupView

    def __init__(self, parent: QWidget) -> None:
        self.__view = GenerateMazeGroupView(parent)
        self.__view.onMazeSpecChosen.connect(self.__onGenerateButtonPressed)

    def showView(self) -> None:
        self.__view.show()
    
    def __onGenerateButtonPressed(self, mazeSpec: MazeGenerationSpecification) -> None:
        
