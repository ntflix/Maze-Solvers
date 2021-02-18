from modules.user_interface.ui_translation_data_structures.maze_generation_specification import (
    MazeGenerationSpecification,
)
from typing import Any, Callable, Optional, Tuple
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
    def __init__(
        self,
        onGenerateButtonPressed: Callable[
            [MazeGenerationSpecification],
            None,
        ],
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for generating mazes
        """
        super().__init__(parent=parent, *args, **kwargs)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        groupbox = QGroupBox("Generate Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        mazeSizePicker = self.__getMazeSizePickerLayout()

        simplyConnectedCheckbox = QCheckBox()
        simplyConnectedCheckbox.setChecked(True)

        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(onGenerateButtonPressed)  # type: ignore

        vbox.addRow("Size", mazeSizePicker)
        vbox.addRow("Simply Connected", simplyConnectedCheckbox)
        vbox.addRow(generateButton)

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