import sys

from PySide6 import QtWidgets

from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.ui.MainWindow import MainWindow


class MainApp(metaclass=Singleton):  # pylint: disable=too-few-public-methods
    """
    Initial runner for the app, container for the state of the main Qt runner, and the main window
    """

    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])

        self.mainWindow = MainWindow()
        self.mainWindow.resize(800, 600)

    def run(self) -> None:
        """
        Runs the app
        """
        self.mainWindow.show()
        sys.exit(self.app.exec())

    def getMainWindow(self) -> MainWindow:  # pylint: disable=missing-function-docstring
        return self.mainWindow
