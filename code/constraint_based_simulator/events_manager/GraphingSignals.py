from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


signalSetSpeed: Signal[SimulationSpeeds] = Signal[SimulationSpeeds]()
signalPause: Signal[bool] = Signal[bool]()
signalRefresh: Signal[float] = Signal[float]()
signalStep: Signal = Signal()
signalRequestState: Signal = Signal()
signalNewFrame: Signal = Signal()