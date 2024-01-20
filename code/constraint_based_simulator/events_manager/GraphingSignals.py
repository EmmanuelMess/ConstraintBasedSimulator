from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.simulator.SimulationData import SimulationData
from constraint_based_simulator.ui.SimulationSpeeds import SimulationSpeeds


signalSetSpeed: Signal[SimulationSpeeds] = Signal[SimulationSpeeds]()
signalPause: Signal[bool] = Signal[bool]()
signalRefresh: Signal[float] = Signal[float]()
signalStep: Signal[float] = Signal[float]()
signalRequestState: Signal[SimulationData] = Signal[SimulationData]()
signalNewFrame: Signal[DrawableScene] = Signal[DrawableScene]()
