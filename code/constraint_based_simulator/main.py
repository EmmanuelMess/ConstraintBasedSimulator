from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.ui.MainApp import MainApp


def main():
    """
    Start basic components that cannot be started in other parts, in development, used to call functions that
    act as scaffolding for missing modules
    """
    InitializationSignals.appInitialization.emit()
    return MainApp().run()


if __name__ == '__main__':
    main()
