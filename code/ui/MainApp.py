import sys

from PySide6 import QtWidgets

from common.Singleton import Singleton
from ui.MainWindow import MainWindow


class MainApp(metaclass=Singleton):

    def run(self):
        app = QtWidgets.QApplication([])

        widget = MainWindow()
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
