from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from typing import Any, List, Optional, Tuple
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class AgentLogView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The 'Log' window view. Shows the current state of the solver at top, and for each history item:
            Left: Human description of command
            Right: Result success or not
        """
        # initialize the solver state history list to a new list
        super(AgentLogView, self).__init__(parent=parent, *args, **kwargs)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        verticalGroupLayout = QVBoxLayout()
        self.__currentStateBox = CurrentStateBox("Not set…")
        verticalGroupLayout.addWidget(self.__currentStateBox)

        # define the vertical scroll area of the log
        logLayoutScrollArea = QScrollArea()
        # enable smart vertical scroll
        logLayoutScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        # disable horizontal scroll
        logLayoutScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # define our log layout (name on left, result on right) and add to layout
        self.__verticalLogLayout = VerticalLogLayout()
        logLayoutScrollArea.setWidget(self.__verticalLogLayout)

        # add the log layout to the vertical layout
        verticalGroupLayout.addWidget(logLayoutScrollArea)

        layout.addLayout(verticalGroupLayout)

        self.setLayout(layout)
        self.setWindowTitle("Agent Log")

    def onLogUpdate(self, logItems: List[MazeSolverCommand]) -> None:

        commandsAndResults: List[Tuple[str, str]] = []
        for logItem in logItems:
            # safely unwrap optional MazeSolverCommandResult value
            resultDescription = ""
            if logItem.commandResult is not None:
                resultDescription = logItem.commandResult.humanDescription
            else:
                resultDescription = ""

            commandsAndResults.append((logItem.humanDescription, resultDescription))

        # update the log layout
        self.__verticalLogLayout.updateCommands(commandsAndResults)
        self.update()

    def onStateUpdate(self, state: str) -> None:
        self.__currentStateBox.onStateChange(state)
        self.update()


class VerticalLogLayout(QWidget):
    __commandNames: List[str] = []
    __commandResults: List[str] = []

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The log layout consisting of, for each command:
            Left: Command name
            Right: Command result
        """
        super(VerticalLogLayout, self).__init__(parent=parent, *args, **kwargs)
        # set layout and add placeholder layouts to ensure they aren't automatically destroyed later
        layout = QHBoxLayout()

        self.__commandNames.append("Command name")
        self.__commandResults.append("Result")

        commandNamesBox = QVBoxLayout()
        commandResultsBox = QVBoxLayout()

        # add the human descriptions text to the layouts
        for i in range(0, len(self.__commandNames)):
            commandNamesBox.addWidget(QLabel(self.__commandNames[i]))
            commandResultsBox.addWidget(QLabel(self.__commandResults[i]))

        layout.addLayout(commandNamesBox)
        layout.addLayout(commandResultsBox)

        # remember to set the layout!
        self.setLayout(layout)

    def updateCommands(self, commands: List[Tuple[str, str]]) -> None:
        """Update the commands/result list with a given (command description, result description) tuple.

        Parameters
        ----------
        command : Tuple[str, str]
            A tuple of a command description and command result.
            For example:
                ("Move forward", "OK"), or
                ("Check forward", "Not clear")
        """

        for command in commands:
            self.__commandNames.append(command[0])
            self.__commandResults.append(command[1])

        self.update()


class CurrentStateBox(QWidget):
    def __init__(
        self,
        state: str,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The horizontal box of the current state of the solver.
        """
        super(CurrentStateBox, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        # add "State: " label to layout:
        layout.addWidget(QLabel("State: "))
        # create current state label and add to layout:
        self.__currentStateLabel = QLabel(state)
        layout.addWidget(self.__currentStateLabel)

        self.setLayout(layout)

    def onStateChange(self, state: str) -> None:
        self.__currentStateLabel.setText(state)
        self.update()