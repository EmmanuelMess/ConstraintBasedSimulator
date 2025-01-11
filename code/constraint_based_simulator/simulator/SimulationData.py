from dataclasses import dataclass

from typing_extensions import List

from constraint_based_simulator.simulator.NamedParticle import NamedParticle


@dataclass
class SimulationData:
    """
    This is a copy of ParticlesHolder, as the particles give perfect information for the whole simulation
    """
    particles: List[NamedParticle]
