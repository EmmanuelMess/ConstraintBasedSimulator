from dataclasses import dataclass

from typing_extensions import List, Tuple

from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from simulator.Particle import Particle


@dataclass
class SimulationData:
    """
    This is a copy of ParticlesHolder, as the particles give perfect information for the whole simulation
    """
    particles: List[Tuple[Particle, Identifier]]
