import numpy as np

from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.constraints.Constraint import Constraint
from constraint_based_simulator.simulator.constraints.functions.DistanceConstraintFunctions import DistanceConstraintFunctions


class DistanceConstraint(Constraint):
    distance: np.float64

    def __init__(self, particleA: Particle, particleB: Particle, distance: np.float64):
        super(DistanceConstraint, self).__init__([particleA, particleB], DistanceConstraintFunctions().constraintAndDerivativeOfTime,
                         DistanceConstraintFunctions().dConstraint, DistanceConstraintFunctions().d2Constraint)
        self.distance = distance

    def getArgs(self) -> dict:
        return {
            "distance": self.distance
        }
