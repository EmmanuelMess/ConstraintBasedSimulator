from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.ui.MainApp import MainApp


class UiEventsHandler(EventsHandler, metaclass=Singleton):
    """
    Handles all the signals for the ui module
    """

    def __init__(self):
        super().__init__()
        InitializationSignals.appInitialization.connect(self.initializeUi)
        GraphingSignals.signalNewFrame.connect(self.onNewFrame)

    def initializeUi(self):  # pylint: disable=missing-function-docstring
        MainApp().run()

    def onNewFrame(self, drawableScene: DrawableScene):  # pylint: disable=missing-function-docstring
        MainApp().getMainWindow().newFrame.emit(drawableScene)
