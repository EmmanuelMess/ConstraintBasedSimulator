from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile


class UiEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.appInitialization.connect(self.readSimulationFile)

    def readSimulationFile(self):
        simulationFile = SimulationFile("../../examples/example3.simulation")
        # TODO load properties
        InitializationSignals.readFileProperties.emit()