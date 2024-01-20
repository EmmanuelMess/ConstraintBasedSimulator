import numpy as np

from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.constraints.Constraint import Constraint
from constraint_based_simulator.simulator.constraints.functions.CircleConstraintFunctions\
    import CircleConstraintFunctions


class CircleConstraint(Constraint):
    radius: np.float64

    def __init__(self, particle: Particle, center: np.ndarray, radius: np.float64):
        super().__init__([particle], CircleConstraintFunctions().constraintAndDerivativeOfTime,
                         CircleConstraintFunctions().dConstraint, CircleConstraintFunctions().d2Constraint)
        self.center = center
        self.radius = radius

    def getArgs(self) -> dict:
        return {
            "center": self.center,
            "radius": self.radius
        }
