from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.simulator import SimulationHolder


class GrapherEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.simulatorLoaded.connect(self.onSimulatorLoaded)
        GraphingSignals.signalRequestState.connect(self.onSimulationResult)

    def onSimulatorLoaded(self):
        # TODO is this needed?
        pass

    def onSimulationResult(self):
        # TODO generate frame
        GraphingSignals.signalNewFrame.emit()
