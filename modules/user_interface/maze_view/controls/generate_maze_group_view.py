from modules.data_structures.maze.maze import Maze
from modules.data_structures.maze.maze_protocol import MazeProtocol
from PyQt6 import QtCore
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class GenerateMazeGroupView(QWidget):
    mazeGenerated = QtCore.pyqtSignal(MazeProtocol)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for generating mazes
        """
        super().__init__(parent=parent, *args, **kwargs)

        layout = QVBoxLayout()

        groupbox = QGroupBox("Generate Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        mazeSizePicker = self.__getMazeSizePickerLayout()

        simplyConnectedCheckbox = QCheckBox()
        simplyConnectedCheckbox.setChecked(True)

        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(self.__onGenerateButtonPressed)  # type: ignore

        vbox.addRow("Size", mazeSizePicker)
        vbox.addRow("Simply Connected", simplyConnectedCheckbox)
        vbox.addRow(generateButton)

        self.setLayout(layout)
        self.setMinimumSize(300, 150)

    def __getMazeSizePickerLayout(self) -> QHBoxLayout:
        mazeSizePickerLayout = QHBoxLayout()

        xSpinBox = QSpinBox()
        ySpinBox = QSpinBox()

        xSpinBox.setMinimum(2)
        ySpinBox.setMinimum(2)

        xSpinBox.setMaximum(250)
        ySpinBox.setMaximum(250)

        mazeSizePickerLayout.addWidget(xSpinBox)
        mazeSizePickerLayout.addWidget(QLabel("by"))
        mazeSizePickerLayout.addWidget(ySpinBox)

        return mazeSizePickerLayout

    def __onGenerateButtonPressed(self, p0: MazeGenerationSpecification) -> None:
        print("generate button pressed")
        self.mazeGenerated.emit(Maze(10, 10))
        # raise NotImplementedError()
