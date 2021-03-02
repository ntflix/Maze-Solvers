from modules.common_structures.xy import XY
from modules.user_interface.maze_view.controls.xy_size_picker import XYPicker
from PyQt6.QtCore import pyqtSignal
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GenerateMazeGroupView(QWidget):
    onMazeSpecChosen = pyqtSignal(MazeGenerationSpecification)
    __simplyConnectedCheckbox: QCheckBox
    __mazeSizePicker: XYPicker

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        Grouped controls box for generating mazes
        """
        super(GenerateMazeGroupView, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        groupbox = QGroupBox("Generate Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        self.__mazeSizePicker = XYPicker(
            minimum=XY(2, 2),
            maximum=XY(250, 250),
            initialValue=XY(2, 2),
            parent=self,
        )

        self.__simplyConnectedCheckbox = QCheckBox()
        self.__simplyConnectedCheckbox.setChecked(True)

        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(self.__onGenerateButtonPressed)  # type: ignore

        vbox.addRow("Size", self.__mazeSizePicker)
        vbox.addRow("Simply Connected", self.__simplyConnectedCheckbox)
        vbox.addRow(generateButton)

        self.setLayout(layout)

    def __onGenerateButtonPressed(self) -> None:
        self.onMazeSpecChosen.emit(
            MazeGenerationSpecification(
                self.__mazeSizePicker.getValues(),
                self.__simplyConnectedCheckbox.isChecked(),
            ),
        ),
