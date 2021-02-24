from typing import Any, Optional, Tuple
from PyQt6.QtCore import PYQT_SLOT, Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class SolverWindowsButtonsView(QWidget):
    def __init__(
        self,
        onOpenLogButtonPressed: PYQT_SLOT,
        onAgentVarsButtonPressed: PYQT_SLOT,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The "Open Log" and "Agent Variables" buttons view used for opening those windows.
        """
        super(SolverWindowsButtonsView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # define the buttons
        openLogButton = QPushButton("Open Log")
        agentVarsButton = QPushButton("Agent Variables")

        # connect them to their respective methods
        openLogButton.pressed.connect(onOpenLogButtonPressed)  # type: ignore
        agentVarsButton.pressed.connect(onAgentVarsButtonPressed)  # type: ignore

        layout.addWidget(openLogButton)
        layout.addWidget(agentVarsButton)

        layout.setAlignment(openLogButton, Qt.Alignment.AlignHCenter)
        layout.setAlignment(agentVarsButton, Qt.Alignment.AlignHCenter)

        self.setLayout(layout)
