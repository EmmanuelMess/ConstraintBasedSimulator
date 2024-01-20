from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile

appInitialization: Signal = Signal()
readFileProperties: Signal = Signal()
grapherParameters: Signal[int, int] = Signal[int, int]()
simulationPropertiesAvailable: Signal[SimulationFile] = Signal[SimulationFile]()
simulatorLoaded: Signal = Signal()
