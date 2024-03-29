from timeit import default_timer as timer
from typing import Callable

import numpy as np
from scipy.optimize import root  # type: ignore

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.SimulationFunctions import SimulationFunctions
from constraint_based_simulator.simulator.constraints.Constraint import Constraint


class Simulation:  # pylint: disable=too-many-instance-attributes
    """
    Manage the state and step running for simulation
    """

    def __init__(self, particles: IndexerIterator[Particle], constraints: IndexerIterator[Constraint],
                 force: Callable[[np.float64], np.ndarray], printData: bool = False) -> None:
        # pylint: disable=too-many-arguments
        self.particles = particles
        self.constraints = constraints
        self.force = force
        self.printData = printData
        self.updateTiming: float = 0.0
        self.simulationTime = np.float64(0)
        self.error = np.float64(0)

        self.update(np.float64(0))  # HACK this is to prevent the compile from running when pressing the "run" button
        # TODO actually make the precompilation run faster

    def update(self, timestep: np.float64) -> None:
        """
        Run internal simulation update.
        :param timestep: Delta time at which the *next* step will be shown
        """

        start = timer()

        if self.printData:
            MAIN_LOGGER.debug("----------")
            MAIN_LOGGER.debug(f"t {self.simulationTime} Δt {timestep}")

        self.simulationTime += timestep

        if self.printData:
            for particle in self.particles:
                MAIN_LOGGER.debug(f"i {particle.index} x {particle.x} v {particle.v}")

        for particle in self.particles:
            if particle.static:
                continue

            particle.aApplied = self.force(self.simulationTime)[particle.index].copy()
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

            particle.x = SimulationFunctions.x(particle.x, particle.v, particle.a, self.simulationTime)
            particle.v = SimulationFunctions.dx(particle.x, particle.v, particle.a, self.simulationTime)

        end = timer()

        self.updateTiming = end - start

    def getRunningTime(self) -> np.float64:  # pylint: disable=missing-function-docstring
        return self.simulationTime
