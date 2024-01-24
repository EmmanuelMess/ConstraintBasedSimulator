from __future__ import annotations

from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.events_manager.SimpleSignal import SimpleSignal
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile

appInitialization: SimpleSignal = SimpleSignal()
grapherParameters: Signal[int, int] = Signal[int, int]()
simulationPropertiesAvailable: Signal[SimulationFile] = Signal[SimulationFile]()
simulatorLoaded: SimpleSignal = SimpleSignal()
