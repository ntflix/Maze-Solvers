from modules.user_interface.maze_view.controls.solver_windows_buttons_view import (
    SolverWindowsButtonsView,
)
from modules.user_interface.maze_view.controls.labelled_icon_button import (
    LabelledIconButton,
)
from typing import Any, Optional, Tuple
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    PYQT_SLOT,
    QHBoxLayout,
    QLabel,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class SolverControlsView(QWidget):
    def __init__(
        self,
        onPlayButtonPressed: PYQT_SLOT,
        onPauseButtonPressed: PYQT_SLOT,
        onStepButtonPressed: PYQT_SLOT,
        onRestartButtonPressed: PYQT_SLOT,
        onSpeedControlValueChanged: PYQT_SLOT,
        onOpenLogButtonPressed: PYQT_SLOT,
        onAgentVarsButtonPressed: PYQT_SLOT,
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

        stateControlBoxView = SolverControlButtonsView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            parent=self,
        )

        speedControl = MazeSolverSpeedControlView(
            onValueChanged=onSpeedControlValueChanged,
            parent=self,
        )

        solverWindowsButtons = SolverWindowsButtonsView(
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            parent=self,
        )

        layout.addWidget(stateControlBoxView)
        layout.addWidget(speedControl)
        layout.addWidget(solverWindowsButtons)

        self.setLayout(layout)


class SolverControlButtonsView(QWidget):
    # onPlayButtonPressed = pyqtSignal(bool)
    # onPauseButtonPressed = pyqtSignal(bool)
    # onStepButtonPressed = pyqtSignal(bool)
    # onRestartButtonPressed = pyqtSignal(bool)

    def __init__(
        self,
        onPlayButtonPressed: PYQT_SLOT,
        onPauseButtonPressed: PYQT_SLOT,
        onStepButtonPressed: PYQT_SLOT,
        onRestartButtonPressed: PYQT_SLOT,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        The play, pause, step and restart buttons for the solver
        """
        super(SolverControlButtonsView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)

        ###
        ### Play, pause, step and restart buttons
        ###

        playButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_MediaPlay,
            labelText="Play",
            parent=self,
        )
        playButton.onButtonPressed.connect(onPlayButtonPressed)  # type: ignore

        pauseButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_MediaPause,
            labelText="Pause",
            parent=self,
        )
        pauseButton.onButtonPressed.connect(onPauseButtonPressed)  # type: ignore

        stepButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_ArrowForward,
            labelText="Step",
            parent=self,
        )
        stepButton.onButtonPressed.connect(onStepButtonPressed)  # type: ignore

        restartButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_BrowserReload,
            labelText="Restart",
            parent=self,
        )
        restartButton.onButtonPressed.connect(onRestartButtonPressed)  # type: ignore

        buttonsLayout.addWidget(playButton)
        buttonsLayout.addWidget(pauseButton)
        buttonsLayout.addWidget(stepButton)
        buttonsLayout.addWidget(restartButton)

        self.setLayout(buttonsLayout)


class MazeSolverSpeedControlView(QWidget):
    def __init__(
        self,
        onValueChanged: PYQT_SLOT,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Slow/fast slider for maze solver agents speed
        """
        super(MazeSolverSpeedControlView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        slider = QSlider(Qt.Orientations.Horizontal)
        # minimum of 0 op/s
        slider.setMinimum(0)
        # maximum of 50 op/s
        slider.setMaximum(50)
        # initial value in the middle
        slider.setValue(25)

        # slow/fast horizontal labels view
        slowFastLabelsLayout = QHBoxLayout()
        slowFastLabelsLayout.setContentsMargins(0, 0, 0, 0)

        slowLabel = QLabel("Slow")
        fastLabel = QLabel("Fast")

        slowFastLabelsLayout.addWidget(slowLabel)
        slowFastLabelsLayout.addStretch()
        slowFastLabelsLayout.addWidget(fastLabel)

        layout.addWidget(slider)
        layout.addLayout(slowFastLabelsLayout)

        self.setLayout(layout)