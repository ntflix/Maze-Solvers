from modules.user_interface.agent_windows.agent_variables_group_view import (
    AgentVariablesGroupView,
)
from typing import Any, Optional, Tuple
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QWidget


class AgentVariablesView(QWidget):
    onSolverVariablesChange = pyqtSignal(dict)

    def __init__(
        self,
        # The variables are a dictionary of (strings: (var type, value))
        variables: dict[str, tuple[type, Any]],
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The 'Agent Variables' window view. Shows the name of each variable in the left column, and value in the right.
        """
        super(AgentVariablesView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        self.__variablesLayoutView = AgentVariablesGroupView(variables, self)
        layout = QGridLayout()
        layout.addWidget(self.__variablesLayoutView)
        self.setLayout(layout)

        self.setWindowTitle("Agent Variables")

        self.onSolverVariablesChange.connect(
            self.__variablesLayoutView.onVariablesChange
        )
