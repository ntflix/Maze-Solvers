from modules.user_interface.maze_view.controls.labelled_icon_button import (
    LabelledIconButton,
)
from typing import Any, Optional, Tuple
from PyQt6.QtCore import Qt
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

        stateControlBoxView = SolverControlButtonsView(self)
        speedControl = MazeSolverSpeedControlView(self)

        layout.addWidget(stateControlBoxView)
        layout.addWidget(speedControl)


class SolverControlButtonsView(QWidget):
    def __onPlayButtonPressed(self) -> None:
        print("play pressed")

    def __onPauseButtonPressed(self) -> None:
        print("pause pressed")

    def __onStepButtonPressed(self) -> None:
        print("play pressed")

    def __onRestartButtonPressed(self) -> None:
        print("restart pressed")

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Description
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
        playButton.onButtonPressed.connect(  # type: ignore
            self.__onPlayButtonPressed,
        )

        pauseButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_MediaPause,
            labelText="Pause",
            parent=self,
        )
        pauseButton.onButtonPressed.connect(  # type: ignore
            self.__onPauseButtonPressed,
        )

        stepButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_ArrowForward,
            labelText="Step",
            parent=self,
        )
        stepButton.onButtonPressed.connect(  # type: ignore
            self.__onStepButtonPressed,
        )

        restartButton = LabelledIconButton(
            icon=QStyle.StandardPixmap.SP_BrowserReload,
            labelText="Restart",
            parent=self,
        )
        restartButton.onButtonPressed.connect(  # type: ignore
            self.__onRestartButtonPressed,
        )

        buttonsLayout.addWidget(playButton)
        buttonsLayout.addWidget(pauseButton)
        buttonsLayout.addWidget(stepButton)
        buttonsLayout.addWidget(restartButton)

        self.setLayout(buttonsLayout)


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