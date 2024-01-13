from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager.Signal import Signal


class EventsManager(metaclass=Singleton):  # pylint: disable=too-few-public-methods,disable=missing-class-docstring
    signalSetSpeed: Signal
    signalPause: Signal
    signalRefresh: Signal
    signalStep: Signal
    signalRequestState: Signal
    signalNewFrame: Signal
