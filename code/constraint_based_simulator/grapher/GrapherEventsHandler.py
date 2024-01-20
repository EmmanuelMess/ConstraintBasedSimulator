from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable
from constraint_based_simulator.simulator.SimulationData import SimulationData
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


class GrapherEventsHandler(EventsHandler, metaclass=Singleton):
    """
    Handles all the signals for the grapher module, presenter for the simulator (model-view-presenter pattern)
    """

    def __init__(self):
        super().__init__()
        self.paused: bool = True
        self.speed: SimulationSpeeds = SimulationSpeeds.X1
        self.width: int = 50
        self.height: int = 50

        InitializationSignals.simulatorLoaded.connect(self.onSimulatorLoaded)
        InitializationSignals.grapherParameters.connect(self.onGrapherParameters)
        GraphingSignals.signalSetSpeed.connect(self.onSetSpeed)
        GraphingSignals.signalPause.connect(self.onPause)
        GraphingSignals.signalRefresh.connect(self.onRefresh)
        GraphingSignals.signalRequestState.connect(self.onSimulationResult)

    def onSimulatorLoaded(self):  # pylint: disable=missing-function-docstring
        # TODO is this needed?
        pass

    def onGrapherParameters(self, width: int, height: int):  # pylint: disable=missing-function-docstring
        self.width = width
        self.height = height

    def onSetSpeed(self, speed: SimulationSpeeds):  # pylint: disable=missing-function-docstring
        self.speed = speed

    def onPause(self, isPaused: bool):  # pylint: disable=missing-function-docstring
        self.paused = isPaused

    def onRefresh(self, currentTime: float):  # pylint: disable=missing-function-docstring
        if not self.paused:
            GraphingSignals.signalStep.emit(currentTime)

    def onSimulationResult(self, simulationData: SimulationData):  # pylint: disable=missing-function-docstring
        drawableScene = DrawableScene([])

        # TODO this is for testing, move it out to its own class and deal with correct placing in window
        for particle in simulationData.particles:
            drawableScene.allDrawables.append(PointDrawable(int(particle.x[0]), int(particle.x[1])))

        GraphingSignals.signalNewFrame.emit(drawableScene)
