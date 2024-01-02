import sys

from PySide6 import QtWidgets

from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.ui.MainWindow import MainWindow


class MainApp(metaclass=Singleton):

    def run(self):
        app = QtWidgets.QApplication([])

        widget = MainWindow()
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
