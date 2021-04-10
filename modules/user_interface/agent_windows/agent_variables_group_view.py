from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal


class AgentVariablesGroupView(QWidget):
    onVariablesChange = pyqtSignal(dict)

    def __init__(
        self,
        variables: dict[str, tuple[type, Any]],
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The two vertical box layouts of the variable names and their respective values.
        """
        super(AgentVariablesGroupView, self).__init__(parent=parent, *args, **kwargs)
        self.__variables = variables
        self.setContentsMargins(0, 0, 0, 0)
        # keep our name and value labels here so we can destroy them when we need to redraw with updated variables
        namesLabels = list[QLabel]()
        valuesLabels = list[QLabel]()

        self.__horizontalGroupBoxLayout = QHBoxLayout()
        self.__variableNamesBox = QVBoxLayout()
        self.__variableValuesBox = QVBoxLayout()

        # submethod to update the 'names' and 'values' vertical views properly
        def updateVariableViews(vars: dict[str, tuple[type, Any]]) -> None:
            # for each name label in the list of namelabel widgets,
            for nameLabel in namesLabels:
                # then clear the label so it doesn't redraw later…
                nameLabel.clear()
                # and remove it from the vertical box layout.
                self.__variableNamesBox.removeWidget(nameLabel)

            # for each value label in the list of valuelabel widgets,
            for valueLabel in valuesLabels:
                # then clear the label so it doesn't redraw later…
                valueLabel.clear()
                # and remove it from the vertical box layout.
                self.__variableValuesBox.removeWidget(valueLabel)

            self.__variables = vars

            # for each variable name, then…
            # make a copy of the KeysView (keys) so it won't unexpectedly change size during iteration
            currentKeys = list(self.__variables.keys())
            for variableName in currentKeys:
                # add it to the list of label widgets as a QLabel
                namesLabels.append(QLabel(variableName))
                # …also add it to the vertical labelNames labels box
                self.__variableNamesBox.addWidget(namesLabels[-1])

            # for each variable value, then…
            for variableValue in self.__variables.values():
                # add it to the list of label widgets as a QLabel
                valuesLabels.append(QLabel(str(variableValue)))
                # …also add it to the vertical labelValues labels box
                self.__variableValuesBox.addWidget(valuesLabels[-1])

            # add the layouts to our main window layout
            self.__horizontalGroupBoxLayout.addLayout(self.__variableNamesBox)
            self.__horizontalGroupBoxLayout.addLayout(self.__variableValuesBox)

            # aaand finally update the window to reflect our changes.
            self.update()

        self.onVariablesChange.connect(updateVariableViews)
        updateVariableViews(self.__variables)

        self.setLayout(self.__horizontalGroupBoxLayout)
