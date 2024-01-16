from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile

appInitialization: Signal = Signal()
readFileProperties: Signal = Signal()
simulationPropertiesAvailable: Signal[SimulationFile] = Signal[SimulationFile]()
simulatorLoaded: Signal = Signal()
