from modules.user_interface.maze_view.controls.solver_windows_buttons_view import (
    SolverWindowsButtonsView,
)
from modules.user_interface.maze_view.controls.labelled_icon_button import (
    LabelledIconButton,
)
from typing import Any, Optional, Tuple
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
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
        onPlayButtonPressed: pyqtSlot(),
        onPauseButtonPressed: pyqtSlot(),
        onStepButtonPressed: pyqtSlot(),
        onRestartButtonPressed: pyqtSlot(),
        onSpeedControlValueChanged: pyqtSlot(int),
        onOpenLogButtonPressed: pyqtSlot(),
        onAgentVarsButtonPressed: pyqtSlot(),
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

        self.__stateControlBoxView = SolverControlButtonsView(
            onPlayButtonPressed=onPlayButtonPressed,
            onPauseButtonPressed=onPauseButtonPressed,
            onStepButtonPressed=onStepButtonPressed,
            onRestartButtonPressed=onRestartButtonPressed,
            parent=self,
        )

        self.__speedControl = MazeSolverSpeedControlView(
            onValueChanged=onSpeedControlValueChanged,
            parent=self,
        )

        self.__solverWindowsButtons = SolverWindowsButtonsView(
            onOpenLogButtonPressed=onOpenLogButtonPressed,
            onAgentVarsButtonPressed=onAgentVarsButtonPressed,
            parent=self,
        )

        layout.addWidget(self.__stateControlBoxView)
        layout.addWidget(self.__speedControl)
        layout.addWidget(self.__solverWindowsButtons)

        self.setLayout(layout)

    def setMazeSolverControlsEnabled(self, enabled: bool) -> None:
        self.__stateControlBoxView.setEnabled(enabled)
        self.__speedControl.setEnabled(enabled)
        self.__solverWindowsButtons.setEnabled(enabled)


class SolverControlButtonsView(QWidget):
    def __init__(
        self,
        onPlayButtonPressed: pyqtSlot(),
        onPauseButtonPressed: pyqtSlot(),
        onStepButtonPressed: pyqtSlot(),
        onRestartButtonPressed: pyqtSlot(),
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

        self.__playButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_MediaPlay,
            labelText="Play",
            parent=self,
        )
        self.__playButton.onButtonPressed.connect(onPlayButtonPressed)  # type: ignore

        self.__pauseButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_MediaPause,
            labelText="Pause",
            parent=self,
        )
        self.__pauseButton.onButtonPressed.connect(onPauseButtonPressed)  # type: ignore

        self.__stepButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_ArrowForward,
            labelText="Step",
            parent=self,
        )
        self.__stepButton.onButtonPressed.connect(onStepButtonPressed)  # type: ignore

        self.__restartButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_BrowserReload,
            labelText="Restart",
            parent=self,
        )
        self.__restartButton.onButtonPressed.connect(onRestartButtonPressed)  # type: ignore

        buttonsLayout.addWidget(self.__playButton)
        buttonsLayout.addWidget(self.__pauseButton)
        buttonsLayout.addWidget(self.__stepButton)
        buttonsLayout.addWidget(self.__restartButton)

        self.setLayout(buttonsLayout)


class MazeSolverSpeedControlView(QWidget):
    def __init__(
        self,
        onValueChanged: pyqtSlot(int),
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