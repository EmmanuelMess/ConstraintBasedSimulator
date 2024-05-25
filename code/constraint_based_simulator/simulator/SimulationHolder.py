from typing_extensions import Union

from simulator.Simulation import Simulation

simulation: Union[Simulation, None] = None
"""
Holds the current simulation, or none if it has not been loaded yet
"""
