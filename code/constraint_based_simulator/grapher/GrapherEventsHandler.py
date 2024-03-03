from typing_extensions import List

from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.grapher import GenerateDrawables
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile
from constraint_based_simulator.input_reader.ast.GraphicalElement import GraphicalElement
from constraint_based_simulator.simulator.SimulationData import SimulationData
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


class GrapherEventsHandler(EventsHandler, metaclass=Singleton):
    """
    Handles all the signals for the grapher module, presenter for the simulator (model-view-presenter pattern)
    """

    def __init__(self) -> None:
        super().__init__()
        self.paused: bool = True
        self.speed: SimulationSpeeds = SimulationSpeeds.X1
        self.width: int = 50
        self.height: int = 50
        self.graphicalElements: List[GraphicalElement] = []

        InitializationSignals.simulationPropertiesAvailable.connect(self.onSimulationPropertiesAvailable)
        InitializationSignals.simulatorLoaded.connect(self.onSimulatorLoaded)
        InitializationSignals.grapherParameters.connect(self.onGrapherParameters)
        GraphingSignals.signalSetSpeed.connect(self.onSetSpeed)
        GraphingSignals.signalPause.connect(self.onPause)
        GraphingSignals.signalRefresh.connect(self.onRefresh)
        GraphingSignals.signalRequestState.connect(self.onSimulationResult)

    def onSimulationPropertiesAvailable(self, file: SimulationFile) \
            -> None:  # pylint: disable=missing-function-docstring
        if not file.loadedCorrectly():
            return

        graphics = file.getGraphics()
        assert graphics is not None  # HACK assure mypy that graphics is not None
        self.graphicalElements = graphics

    def onSimulatorLoaded(self) -> None:  # pylint: disable=missing-function-docstring
        GraphingSignals.signalStep.emit(0)  # Sort of hack, tells the simulator to present the simulation as-is,
        # to show it on UI

    def onGrapherParameters(self, width: int, height: int) -> None:  # pylint: disable=missing-function-docstring
        self.width = width
        self.height = height

    def onSetSpeed(self, speed: SimulationSpeeds) -> None:  # pylint: disable=missing-function-docstring
        self.speed = speed

    def onPause(self, isPaused: bool) -> None:  # pylint: disable=missing-function-docstring
        self.paused = isPaused

    def onRefresh(self, currentTime: float) -> None:  # pylint: disable=missing-function-docstring
        if not self.paused:
            GraphingSignals.signalStep.emit(currentTime)

    def onSimulationResult(self, simulationData: SimulationData) -> None:  # pylint: disable=missing-function-docstring
        drawableScene = GenerateDrawables.generateDrawableScene(simulationData.particles, self.graphicalElements)
        GraphingSignals.signalNewFrame.emit(drawableScene)
