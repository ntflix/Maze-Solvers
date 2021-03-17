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
# | • Draw line of solver path   | #
# | • Log window view            | #
# | • Check Pledge works!?       | #
# | • Non—Simply Connected       | #
# |——————————————————————————————| #
# |—Maze Loader screen———————————| #
# | • 'Load Last Maze' button    | #
# | • 'Generate Maze' button     | #
# |—Maze View Window—————————————| #
# | • 'Save' function            | #
# | • 'Load' function            | #
# | • onMazeSolved method        | #
# | • Generate maze button       | #
# |—Solver controls——————————————| #
# | • Play button                | #
# | • Pause button               | #
# | • Slow/fast slider           | #
# |——————————————————————————————| #
