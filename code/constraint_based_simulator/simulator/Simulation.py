from timeit import default_timer as timer
from typing import Callable

import numpy as np
from scipy.optimize import root  # type: ignore

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.SimulationFunctions import SimulationFunctions
from constraint_based_simulator.simulator.constraints.Constraint import Constraint


class Simulation:
    """
    Manage the state and step running for simulation
    """

    def __init__(self, particles: IndexerIterator[Particle], constraints: IndexerIterator[Constraint],
                 timestep: np.float64, force: Callable[[np.float64], np.ndarray], printData: bool = False) -> None:
        self.particles = particles
        self.constraints = constraints
        self.timestep = timestep
        self.force = force
        self.printData = printData
        self.updateTiming: float = 0.0
        self.t = np.float64(0)
        self.error = np.float64(0)

    def update(self) -> None:
        start = timer()

        if self.printData:
            MAIN_LOGGER.debug("----------")
            MAIN_LOGGER.debug(f"t {self.t}")

        if self.printData:
            for particle in self.particles:
                MAIN_LOGGER.debug(f"i {particle.index} x {particle.x} v {particle.v}")

        for particle in self.particles:
            if particle.static:
                continue

            particle.aApplied = self.force(self.t)[particle.index].copy()
            particle.a = particle.aApplied.copy()

        lagrangeArgs, lagrange = SimulationFunctions.matrices(self.particles, self.constraints)
        dq, Q, W, J, dJ, C, dC, _, _ = lagrangeArgs

        res = root(lagrange, x0=np.zeros(len(self.constraints), dtype=np.float64), method='lm', args=lagrangeArgs)

        aConstraint = SimulationFunctions.precompiledForceCalculation(J, res.x)

        self.error = np.sqrt(np.sum(lagrange(res.x, *lagrangeArgs)**2))

        if self.printData:
            MAIN_LOGGER.debug(f"dq {dq}")
            MAIN_LOGGER.debug(f"Q {Q}")
            MAIN_LOGGER.debug(f"W {W}")
            MAIN_LOGGER.debug(f"J {J}")
            MAIN_LOGGER.debug(f"dJ {dJ}")

            MAIN_LOGGER.debug(f"J W J.T {J @ W @ J.T}")
            MAIN_LOGGER.debug(f"dJ dq {dJ @ dq}")
            MAIN_LOGGER.debug(f"JWQ {J @ W @ Q}")
            MAIN_LOGGER.debug(f"C {C}")
            MAIN_LOGGER.debug(f"dC {dC}")

            MAIN_LOGGER.debug(f"l {res.x}")
            MAIN_LOGGER.debug(f"f {lagrange(res.x, *lagrangeArgs)}")

        for particle in self.particles:
            if particle.static:
                continue

            particle.aConstraint = aConstraint[particle.index].copy()
            particle.a = particle.aApplied + particle.aConstraint

            if self.printData:
                MAIN_LOGGER.debug(f"i {particle.index} ~a + ^a = a"
                                  f" {particle.aApplied} {particle.aConstraint} {particle.a}")

            particle.x = SimulationFunctions.x(particle.x, particle.v, particle.a, self.t)
            particle.v = SimulationFunctions.dx(particle.x, particle.v, particle.a, self.t)

        end = timer()

        self.updateTiming = end - start
        self.t += self.timestep

    def getRunningTime(self) -> np.float64:  # pylint: disable=missing-function-docstring
        return self.t
