import sys

from PySide6 import QtWidgets

from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.ui.MainWindow import MainWindow


class MainApp(metaclass=Singleton):  # pylint: disable=too-few-public-methods
    """
    Initial runner for the app, container for the state of the main Qt runner, and the main window
    """

    def run(self) -> None:
        """
        Runs the app
        """
        app = QtWidgets.QApplication([])

        widget = MainWindow()
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
