from modules.ui_processing_link_layer.ui_state_model import (
    UIStateModel,
)
import logging

if __name__ == "__main__":
    #  set up logging of error messages in case any occur
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LEVEL = logging.ERROR
    logging.basicConfig(format=FORMAT, level=LEVEL)
    log = logging.getLogger()

    #  instantiate app and start it
    app = UIStateModel()
    statusCode = app.startApplication()
    # return the status code (normal status codes - 0 for ok, but anything else?? who knows)
    exit(statusCode)

# |——————————————————————————————| #
# |~~~~~~~~~~~~~TODO~~~~~~~~~~~~~| #
# |——————————————————————————————| #
# |—Urgent———————————————————————| #
# | • Draw line of solver path   | #
# | • Log window view autoupdate | #
# |——————————————————————————————| #
# |—Maze View Window—————————————| #
# | • 'Save' function            | #
# | • 'Load' function            | #
# | • onMazeSolved method        | #
# | • 'Clear' funct. (see reqs)  | #
# | • Alert on solver finish     | #
# |——————————————————————————————| #
