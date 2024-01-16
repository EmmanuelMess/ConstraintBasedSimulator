from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile


class InputReaderEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.appInitialization.connect(self.readSimulationFile)

    def readSimulationFile(self):
        simulationFile = SimulationFile("../../examples/example3.simulation")
        if not simulationFile.loadedCorrectly():
            MAIN_LOGGER.error(f"File loaded incorrectly")
            return

        InitializationSignals.simulationPropertiesAvailable.emit(simulationFile)
