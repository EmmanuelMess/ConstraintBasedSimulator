from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler


class UiEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.appInitialization.connect(self.initializeUi)

    def initializeUi(self):
        pass
