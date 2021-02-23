from modules.user_interface.maze_view.controls.xy_size_picker import XYPicker
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
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import logging


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
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        groupbox = QGroupBox("Generate Maze")
        layout.addWidget(groupbox)

        vbox = QFormLayout()
        groupbox.setLayout(vbox)

        mazeSizePicker = XYPicker(self)

        simplyConnectedCheckbox = QCheckBox()
        simplyConnectedCheckbox.setChecked(True)

        generateButton = QPushButton("Generate")
        generateButton.clicked.connect(  # type: ignore
            lambda: self.__onGenerateButtonPressed(
                p0=MazeGenerationSpecification(
                    size=mazeSizePicker.getValues(),
                    simplyConnected=simplyConnectedCheckbox.isChecked(),
                ),
            )
        )

        vbox.addRow("Size", mazeSizePicker)
        vbox.addRow("Simply Connected", simplyConnectedCheckbox)
        vbox.addRow(generateButton)

        self.setLayout(layout)

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
