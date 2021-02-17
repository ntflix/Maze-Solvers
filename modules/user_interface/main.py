# PyQt6 file for user interface test

from modules.data_structures.maze.maze import Maze
from modules.user_interface.maze_view.maze_view import MazeView
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Maze Solvers")

layout = QHBoxLayout()
layout2 = QVBoxLayout()

maze = Maze(10, 10)

layout.addWidget(MazeView(maze=maze))
layout.addLayout(layout2)

layout2.addWidget(
    QPushButton("Epic"),
)

layout2.addWidget(
    QPushButton("Epic"),
)

layout2.setAlignment(layout2, Qt.Alignment.AlignTop)
layout2.addStretch(0)

window.setLayout(layout)
window.show()
app.exec()
