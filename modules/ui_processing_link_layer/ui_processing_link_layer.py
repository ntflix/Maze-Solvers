from modules.ui_processing_link_layer.ui_state_model import UIStateModel


class UIProcessingLinkLayer:
    __stateModel: UIStateModel

    def __init__(self) -> None:
        self.__stateModel = UIStateModel()

    def start(self) -> int:
        return self.__stateModel.startApplication()


if __name__ == "__main__":
    import logging

    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LEVEL)
    log = logging.getLogger()

    app = UIProcessingLinkLayer()
    app.start()

# |——————————————————————————————| #
# |~~~~~~~~~~~~~TODO~~~~~~~~~~~~~| #
# |——————————————————————————————| #
# |—Urgent———————————————————————| #
# | • Log window view            | #
# | • Draw line of solver path   | #
# | • Make solver stop if solved | #
# |——————————————————————————————| #
# |—Maze View Window—————————————| #
# | • 'Save' function            | #
# | • 'Load' function            | #
# | • onMazeSolved method        | #
# |——————————————————————————————| #
