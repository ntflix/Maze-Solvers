from modules.user_interface.main_window import MazeSolverUI
from modules.ui_processing_link_layer.ui_state_model import UIStateModel


class UIProcessingLinkLayer:
    __stateModel: UIStateModel

    def __init__(self) -> None:
        ui = self.__initUI()
        self.__stateModel = UIStateModel(ui)

    def start(self) -> int:
        return self.__startUI()

    def __initUI(self) -> MazeSolverUI:
        userInterface = MazeSolverUI()
        return userInterface

    def __startUI(self) -> int:
        return self.__stateModel.startApplication()


app = UIProcessingLinkLayer()
app.start()
