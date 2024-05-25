from constraint_based_simulator.events_manager import InitializationSignals, EventsHandlersLoader
from constraint_based_simulator.ui.MainApp import MainApp


def main() -> None:
    """
    Start basic components that cannot be started in other parts, in development, used to call functions that
    act as scaffolding for missing modules
    """
    EventsHandlersLoader.loadEventsHandlers()
    InitializationSignals.appInitialization.emit()
    MainApp().run()


if __name__ == '__main__':
    main()
