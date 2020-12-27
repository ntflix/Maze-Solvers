import datetime

DEBUG_MODE = 2
# DEBUG_MODE modes:
#   0: absolutely nothing
#   1: log to file
#   2: print to console


def debugPrint(_text: str = "") -> None:
    if DEBUG_MODE == 2:
        # print to console
        timestamp = datetime.datetime.now().isoformat()
        print(f"{timestamp}:\t{_text}")
    elif DEBUG_MODE == 1:
        # log to file
        timestamp = datetime.datetime.now().isoformat()
        raise NotImplementedError("logging to file not yet implemented")