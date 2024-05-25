from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from simulator.Particle import Particle


class NamedParticle:
    """
    A particle with an identifier
    """

    def __init__(self, particle: Particle, id: Identifier):
        self.particle = particle
        self.id = id
