# PyQt6 file for user interface test

from modules.user_interface.maze_view import MazeView
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Maze Solvers")

layout = QHBoxLayout()
layout2 = QVBoxLayout()

layout.addWidget(QTextEdit())
layout.addLayout(layout2)

layout2.addWidget(
    QPushButton("Epic"),
)

layout2.addWidget(
    QPushButton("Epic"),
)

layout2.addWidget(
    MazeView(),
)

layout2.setAlignment(layout2, Qt.Alignment.AlignBottom)

window.setLayout(layout)
window.show()
app.exec()