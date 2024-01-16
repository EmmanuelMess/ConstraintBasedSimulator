from constraint_based_simulator.grapher.GrapherEventsHandler import GrapherEventsHandler
from constraint_based_simulator.input_reader.InputReaderEventsHandler import InputReaderEventsHandler
from constraint_based_simulator.simulator.SimulatorEventsHandler import SimulatorEventsHandler
from constraint_based_simulator.ui.UiEventsHandler import UiEventsHandler


def loadEventsHandlers():
    """
    Loads every single module for each of its subclases
    """
    GrapherEventsHandler()
    InputReaderEventsHandler()
    SimulatorEventsHandler()
    UiEventsHandler()
