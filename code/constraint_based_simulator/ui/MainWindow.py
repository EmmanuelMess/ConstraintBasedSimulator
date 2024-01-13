import random
from PySide6 import QtCore, QtWidgets

from constraint_based_simulator.events_manager.EventsManager import EventsManager
from constraint_based_simulator.ui import Strings
from constraint_based_simulator.ui.Speeds import Speeds


class MainWindow(QtWidgets.QWidget):
    """
    Handles state and interaction with the main window of the app
    """

    PAUSED_TEXT: dict[bool, str] = {True: Strings.run, False: Strings.pause}
    SPEED_TEXT: dict[Speeds, str] \
        = {Speeds.X1: Strings.speed1, Speeds.X10: Strings.speed10, Speeds.X100: Strings.speed100}

    def __init__(self):
        super().__init__()

        self.isPaused = True
        self.velocity = Speeds.X1

        self.runButton = QtWidgets.QPushButton(Strings.run)
        self.velocityButton = QtWidgets.QPushButton(Strings.speed1)
        self.text = QtWidgets.QLabel(text="Grapher", parent=self, alignment=QtCore.Qt.AlignCenter)

        self.rootLayout = QtWidgets.QVBoxLayout(self)

        self.topLayout = QtWidgets.QHBoxLayout(self)
        self.topLayout.addWidget(self.runButton)
        self.topLayout.addWidget(self.velocityButton)

        self.rootLayout.addLayout(self.topLayout)
        self.rootLayout.addWidget(self.text)

        self.runButton.clicked.connect(self.onRunButtonClick)
        self.velocityButton.clicked.connect(self.onVelocityButtonClick)

    @QtCore.Slot()
    def onRunButtonClick(self):  # pylint: disable=missing-function-docstring
        self.isPaused = not self.isPaused

        EventsManager.signalPause.emit(self.isPaused)
        self.runButton.setText(MainWindow.PAUSED_TEXT[self.isPaused])

    @QtCore.Slot()
    def onVelocityButtonClick(self):  # pylint: disable=missing-function-docstring
        self.velocity = list(Speeds)[(self.velocity.value + 1) % len(Speeds)]

        EventsManager.signalSetSpeed.emit(self.velocity)
        self.velocityButton.setText(MainWindow.SPEED_TEXT[self.velocity])
