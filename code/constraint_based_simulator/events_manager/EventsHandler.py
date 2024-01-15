from constraint_based_simulator.simulator.SimulatorEventsHandler import SimulatorEventsHandler


class EventsHandler:
    """
    Base class for all module's EventHandlers, ensures that initialization signals are correctly loaded
    """
    def __init__(self):
        """
        Loads every single module for each of its subclases
        """
        SimulatorEventsHandler()
