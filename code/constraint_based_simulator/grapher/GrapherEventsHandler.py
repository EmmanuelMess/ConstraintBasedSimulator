from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.simulator import SimulationHolder
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


class GrapherEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.simulatorLoaded.connect(self.onSimulatorLoaded)
        GraphingSignals.signalSetSpeed.connect(self.onSetSpeed)
        GraphingSignals.signalPause.connect(self.onPause)
        GraphingSignals.signalRefresh.connect(self.onRefresh)
        GraphingSignals.signalRequestState.connect(self.onSimulationResult)

    def onSimulatorLoaded(self):
        # TODO is this needed?
        pass

    def onSetSpeed(self, speed: SimulationSpeeds):
        pass

    def onPause(self, isPaused: bool):
        pass

    def onRefresh(self, currentTime: float):
        GraphingSignals.signalStep.emit(currentTime)

    def onSimulationResult(self):
        # TODO generate frame
        GraphingSignals.signalNewFrame.emit()
