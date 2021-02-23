from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class SolverControlsView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The "Solver Controls…" dropdown view of the solver controls for the active solver
        """
        super(SolverControlsView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        stateControlBoxView = SolverStateControlBox(self)
        speedControl = MazeSolverSpeedControlView(self)

        layout.addWidget(stateControlBoxView)
        layout.addWidget(speedControl)


class SolverStateControlBox(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Description
        """
        super(SolverStateControlBox, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        playButton = QToolButton(self)
        playButton.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay,
            ),
        )

        pauseButton = QToolButton(self)
        pauseButton.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPause,
            ),
        )

        stepButton = QToolButton(self)
        stepButton.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_ArrowForward,
            ),
        )

        restartButton = QToolButton(self)
        restartButton.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_BrowserReload,
            )
        )

        layout.addWidget(playButton)
        layout.addWidget(pauseButton)
        layout.addWidget(stepButton)
        layout.addWidget(restartButton)

        self.setLayout(layout)


class MazeSolverSpeedControlView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Description
        """
        super(MazeSolverSpeedControlView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
