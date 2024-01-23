from __future__ import annotations

from PySide6.QtCore import Slot, QTimer, Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from constraint_based_simulator.events_manager import GraphingSignals
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.ui import Strings
from constraint_based_simulator.ui.GrapherWidget import GrapherWidget
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


class MainWindow(QWidget):  # pylint: disable=too-many-instance-attributes
    """
    Handles state and interaction with the main window of the app
    """

    PAUSED_TEXT: dict[bool, str] = {True: Strings.run, False: Strings.pause}
    SPEED_TEXT: dict[SimulationSpeeds, str] = {
        SimulationSpeeds.X1: Strings.speed1, SimulationSpeeds.X10: Strings.speed10,
        SimulationSpeeds.X100: Strings.speed100
    }

    UPDATE_TICK: int = 16

    newFrame = Signal(DrawableScene)

    def __init__(self) -> None:
        super().__init__()

        self.isPaused = True
        self.velocity = SimulationSpeeds.X1

        self.timer = QTimer(self)
        self.timer.start(MainWindow.UPDATE_TICK)
        self.timer.timeout.connect(self.onUpdateGraph)

        self.runButton = QPushButton(Strings.run)
        self.velocityButton = QPushButton(Strings.speed1)
        self.grapher = GrapherWidget()

        self.rootLayout = QVBoxLayout(self)

        self.topLayout = QHBoxLayout(self)
        self.topLayout.addWidget(self.runButton)
        self.topLayout.addWidget(self.velocityButton)

        self.rootLayout.addLayout(self.topLayout)
        self.rootLayout.addWidget(self.grapher)

        self.runButton.clicked.connect(self.onRunButtonClick)
        self.velocityButton.clicked.connect(self.onVelocityButtonClick)

        self.newFrame.connect(self.grapher.newFrame)

    @Slot()
    def onUpdateGraph(self) -> None:  # pylint: disable=missing-function-docstring
        GraphingSignals.signalRefresh.emit(0)  # TODO add correct time

    @Slot()
    def onRunButtonClick(self) -> None:  # pylint: disable=missing-function-docstring
        self.isPaused = not self.isPaused

        GraphingSignals.signalPause.emit(self.isPaused)
        self.runButton.setText(MainWindow.PAUSED_TEXT[self.isPaused])

    @Slot()
    def onVelocityButtonClick(self) -> None:  # pylint: disable=missing-function-docstring
        self.velocity = list(SimulationSpeeds)[(self.velocity.value + 1) % len(SimulationSpeeds)]

        GraphingSignals.signalSetSpeed.emit(self.velocity)
        self.velocityButton.setText(MainWindow.SPEED_TEXT[self.velocity])
