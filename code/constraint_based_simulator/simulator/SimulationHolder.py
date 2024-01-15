from typing_extensions import Union

from constraint_based_simulator.simulator.Simulation import Simulation


"""
Holds the current simulation, or none if it has not been loaded yet
"""
simulation: Union[Simulation, None] = None