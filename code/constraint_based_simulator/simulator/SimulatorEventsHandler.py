from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.simulator import SimulationHolder
from constraint_based_simulator.simulator.Simulation import Simulation


class SimulatorEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.simulationPropertiesAvailable.connect(self.loadSimulator)

    def loadSimulator(self):
        # TODO load simulation with properties
        SimulationHolder.simulation = Simulation()
        InitializationSignals.simulatorLoaded.emit()

    def step(self):
        if SimulationHolder.simulation is None:
            MAIN_LOGGER.error(f"Simulation update without simulation loaded!")
            return

        SimulationHolder.simulation.update()

        GraphingSignals.signalRequestState.emit()
