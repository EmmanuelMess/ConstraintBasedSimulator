from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager.Signal import Signal
from constraint_based_simulator.ui.Speeds import Speeds


class EventsManager(metaclass=Singleton):  # pylint: disable=too-few-public-methods,disable=missing-class-docstring
    signalSetSpeed: Signal[Speeds] = Signal[Speeds]()
    signalPause: Signal[bool] = Signal[bool]()
    signalRefresh: Signal = Signal()
    signalStep: Signal = Signal()
    signalRequestState: Signal = Signal()
    signalNewFrame: Signal = Signal()
