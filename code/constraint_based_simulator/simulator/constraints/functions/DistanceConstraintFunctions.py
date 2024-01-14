import jax.numpy as jnp

from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.simulator.PositionApproximation import constructPositionFunction
from constraint_based_simulator.simulator.constraints.functions.ConstraintFunctions import ConstraintFunctions


class DistanceConstraintFunctions(metaclass=Singleton):
    @staticmethod
    def constraint(x: jnp.ndarray, params: dict):
        aPosition = x[0]
        bPosition = x[1]
        return jnp.sum((aPosition - bPosition) ** 2) / 2 - (params["distance"] ** 2) / 2

    @staticmethod
    def constraintOfTime(t: jnp.float64, x: jnp.ndarray, v: jnp.ndarray, a: jnp.ndarray, params: dict):
        positionApproximationA = constructPositionFunction(x[0], v[0], a[0])
        positionApproximationB = constructPositionFunction(x[1], v[1], a[1])
        return DistanceConstraintFunctions.constraint(
            jnp.array([positionApproximationA(t), positionApproximationB(t)]), params)  # TODO fix this array() call

    def __init__(self):
        self.constraintAndDerivativeOfTime, self.dConstraint, self.d2Constraint =\
            ConstraintFunctions.computeDerivatives(DistanceConstraintFunctions.constraintOfTime)