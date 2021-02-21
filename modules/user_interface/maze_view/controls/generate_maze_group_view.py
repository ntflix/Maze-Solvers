from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
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
import logging
from modules.common_structures.xy import XY


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

        mazeSizePicker = MazeSizePicker(self)

        simplyConnectedCheckbox = QCheckBox()
        simplyConnectedCheckbox.setChecked(True)

        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(  # type: ignore
            lambda: self.__onGenerateButtonPressed(
                p0=MazeGenerationSpecification(
                    size=XY(
                        mazeSizePicker.getValues()[0],
                        mazeSizePicker.getValues()[0],
                    ),
                    simplyConnected=simplyConnectedCheckbox.isChecked(),
                ),
            )
        )

        vbox.addRow("Size", mazeSizePicker)
        vbox.addRow("Simply Connected", simplyConnectedCheckbox)
        vbox.addRow(generateButton)

        self.setLayout(layout)
        self.setMinimumSize(300, 150)

    def __onGenerateButtonPressed(self, p0: MazeGenerationSpecification) -> None:
        print("generate button pressed")
        maze = self.__generateMaze(mazeSpec=p0)
        self.mazeGenerated.emit(maze)

    def __generateMaze(self, mazeSpec: MazeGenerationSpecification) -> MazeProtocol:
        maze: MazeProtocol
        # log to debug
        logging.debug(
            "Generating a "
            + ("non-" if mazeSpec.simplyConnected else "")
            + f"simply-connected maze of size {mazeSpec.size}."
        )

        if mazeSpec.simplyConnected:
            # generate a simply connected maze
            mazeGenerator = RecursiveBacktracker(mazeSpec.size)
            maze = mazeGenerator.generate()
        else:
            mazeGenerator = RecursiveBacktracker(mazeSpec.size)
            maze = mazeGenerator.generate()
        return maze


from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QWidget


class MazeSizePicker(QWidget):
    __ySpinBox: QSpinBox
    __xSpinBox: QSpinBox

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A horizontal dual spin box widget designed for the XY size of a maze.
        """
        super(MazeSizePicker, self).__init__(parent=parent, *args, **kwargs)

        mazeSizePickerLayout = QHBoxLayout()

        self.__xSpinBox = QSpinBox()
        self.__ySpinBox = QSpinBox()

        self.__xSpinBox.setMinimum(2)
        self.__ySpinBox.setMinimum(2)

        self.__xSpinBox.setMaximum(250)
        self.__ySpinBox.setMaximum(250)

        mazeSizePickerLayout.addWidget(self.__xSpinBox)
        mazeSizePickerLayout.addWidget(QLabel("by"))
        mazeSizePickerLayout.addWidget(self.__ySpinBox)

        self.setLayout(mazeSizePickerLayout)

    def getValues(self) -> Tuple[int, int]:
        """Get the X and Y values of this input widget.

        Returns
        -------
        Tuple[int, int]
            The X and Y values of the number picker spin boxes.
        """
        return (
            self.__xSpinBox.value(),
            self.__ySpinBox.value(),
        )