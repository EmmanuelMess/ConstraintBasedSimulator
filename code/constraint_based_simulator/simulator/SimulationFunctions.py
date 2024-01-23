import numba  # type: ignore
import numpy as np
from typing_extensions import Tuple, Callable

from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.constraints.Constraint import Constraint


class SimulationFunctions:
    """
    See mathematical model
    """

    @staticmethod
    @numba.njit
    def precompiledForceCalculation(J: np.ndarray, l: np.float64) -> np.ndarray:
        """
        Resulting force for the particles (see mathematical model)
        """
        return (J.T @ l).reshape((-1, 2))

    @staticmethod
    @numba.njit
    def precompiledLagrange(l: np.float64, dq: np.ndarray, Q: np.ndarray, W: np.ndarray, J: np.ndarray, dJ: np.ndarray,
                            C: np.ndarray, dC: np.ndarray, ks: np.float64, kd: np.float64) -> np.ndarray:
        """
        Minimization to calculate correct forces as lagrangian multipliers (see mathematical model)
        """
        return ((J @ W @ J.T) * l.T + dJ @ dq + J @ W @ Q + ks * C + kd * dC).reshape((-1,))

    @staticmethod
    def matrices(particles: IndexerIterator[Particle], constraints: IndexerIterator[Constraint],
                 weight: np.float64 = np.float64(1))\
            -> Tuple[
                Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                      np.float64, np.float64],
                Callable[[np.float64, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                          np.ndarray, np.float64, np.float64], np.ndarray]
            ]:
        """
        Compute the matrices to run the lagrangian multipliers (see mathematical model)
        """
        d = 2
        n = len(particles)
        m = len(constraints)
        ks = np.float64(0.1)
        kd = np.float64(1)

        dq = np.zeros((n, d), dtype=np.float64)
        Q = np.zeros((n, d), dtype=np.float64)
        C = np.zeros((m,), dtype=np.float64)
        dC = np.zeros((m,), dtype=np.float64)
        W = np.identity(n * d, dtype=np.float64) * weight
        J = np.zeros((m, n, d), dtype=np.float64)
        dJ = np.zeros((m, n, d), dtype=np.float64)

        for particle in particles:
            dq[particle.index] = particle.v
            Q[particle.index] = particle.a

        dq = dq.reshape((n * d, 1))
        Q = Q.reshape((n * d, 1))

        for constraint in constraints:
            CForConstraint, dCForConstraint, JForConstraint, dJForConstraint = constraint.get()
            C[constraint.index] += CForConstraint
            dC[constraint.index] += dCForConstraint

            # HACK advanced numpy indexing is much faster than the equivalent loop, as jax copies the array values
            # before returning them when using normal indexing
            indicesConstraint = [constraint.index for _ in constraint.particles]
            indicesParticle = [particle.index for particle in constraint.particles]

            J[indicesConstraint, indicesParticle] += JForConstraint
            dJ[indicesConstraint, indicesParticle] += dJForConstraint

        J = J.reshape((m, n * d))
        dJ = dJ.reshape((m, n * d))

        lagrangeArgs = dq, Q, W, J, dJ, C, dC, ks, kd
        return lagrangeArgs, SimulationFunctions.precompiledLagrange

    @staticmethod
    def x(p: np.ndarray, v: np.ndarray, a: np.ndarray, t: np.float64) -> np.ndarray:
        """
        Position Taylor approximation from position, velocity, acceleration and time
        """
        return p + v * t + (1/2) * a * t**2

    @staticmethod
    def dx(p: np.ndarray, v: np.ndarray, a: np.ndarray, t: np.float64) -> np.ndarray:  # pylint: disable=unused-argument
        """
        Derivative of Taylor approximation from position, velocity, acceleration and time
        """
        return v + a * t
