import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("HOASDO")
        self.resize(200, 200)
        self.__add_widgets()

    def __add_widgets(self):
        self.statusBar().showMessage("bruh")

        self.menuBar = QMenuBar()
        self.menuBar.setNativeMenuBar(False)

        fileMenu = self.menuBar.addMenu("&Fidle")
        editMenu = self.menuBar.addMenu("&Eddit")

        action = QAction()
        action.setStatusTip("News File")
        action.setText("aosdoiao")
        fileMenu.addAction(action)
        fileMenu.addSeparator()

        s = self.menuBar.addMenu(fileMenu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())