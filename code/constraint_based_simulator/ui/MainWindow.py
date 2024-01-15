from __future__ import annotations

from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.events_manager import GraphingSignals
from constraint_based_simulator.ui import Strings
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


class MainWindow(QWidget):
    """
    Handles state and interaction with the main window of the app
    """

    PAUSED_TEXT: dict[bool, str] = {True: Strings.run, False: Strings.pause}
    SPEED_TEXT: dict[SimulationSpeeds, str] = {
        SimulationSpeeds.X1: Strings.speed1, SimulationSpeeds.X10: Strings.speed10,
        SimulationSpeeds.X100: Strings.speed100
    }

    UPDATE_TICK: int = 1000

    def __init__(self):
        super().__init__()

        self.isPaused = True
        self.velocity = SimulationSpeeds.X1

        self.timer = QTimer(self)
        self.timer.start(MainWindow.UPDATE_TICK)
        self.timer.timeout.connect(self.onUpdateGraph)

        self.runButton = QPushButton(Strings.run)
        self.velocityButton = QPushButton(Strings.speed1)
        self.text = QLabel(text="Grapher", parent=self, alignment=Qt.AlignCenter)

        self.rootLayout = QVBoxLayout(self)

        self.topLayout = QHBoxLayout(self)
        self.topLayout.addWidget(self.runButton)
        self.topLayout.addWidget(self.velocityButton)

        self.rootLayout.addLayout(self.topLayout)
        self.rootLayout.addWidget(self.text)

        self.runButton.clicked.connect(self.onRunButtonClick)
        self.velocityButton.clicked.connect(self.onVelocityButtonClick)

    @Slot()
    def onUpdateGraph(self):  # pylint: disable=missing-function-docstring
        MAIN_LOGGER.debug("Update called")
        GraphingSignals.signalRefresh.emit()

    @Slot()
    def onRunButtonClick(self):  # pylint: disable=missing-function-docstring
        self.isPaused = not self.isPaused

        GraphingSignals.signalPause.emit(self.isPaused)
        self.runButton.setText(MainWindow.PAUSED_TEXT[self.isPaused])

    @Slot()
    def onVelocityButtonClick(self):  # pylint: disable=missing-function-docstring
        self.velocity = list(SimulationSpeeds)[(self.velocity.value + 1) % len(SimulationSpeeds)]

        GraphingSignals.signalSetSpeed.emit(self.velocity)
        self.velocityButton.setText(MainWindow.SPEED_TEXT[self.velocity])
