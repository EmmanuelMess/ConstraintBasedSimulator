from timeit import default_timer as timer
from typing import Callable

import numpy as np
from scipy.optimize import root

from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.SimulationFunctions import SimulationFunctions
from constraint_based_simulator.simulator.constraints.Constraint import Constraint


class Simulation:
    def __init__(self, particles: IndexerIterator[Particle], constraints: IndexerIterator[Constraint], timestep: np.float64,
                 force: Callable[[np.float64], np.ndarray], printData: bool = False):
        self.particles = particles
        self.constraints = constraints
        self.timestep = timestep
        self.force = force
        self.printData = printData
        self.updateTiming = 0
        self.t = np.float64(0)
        self.error = np.float64(0)

    def update(self):
        start = timer()

        if self.printData:
            print("----------")
            print("t", self.t)

        if self.printData:
            for particle in self.particles:
                print("i", particle.index, "x", particle.x, "v", particle.v)

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
            print("dq", dq)
            print("Q", Q)
            print("W", W)
            print("J", J)
            print("dJ", dJ)

            print("J W J.T", J @ W @ J.T)
            print("dJ dq", dJ @ dq)
            print("JWQ", J @ W @ Q)
            print("C", C)
            print("dC", dC)

            print("l", res.x)
            print("f", lagrange(res.x))

        for particle in self.particles:
            if particle.static:
                continue

            particle.aConstraint = aConstraint[particle.index].copy()
            particle.a = particle.aApplied + particle.aConstraint

            if self.printData:
                print("i", particle.index, "~a + ^a = a", particle.aApplied, particle.aConstraint, particle.a)

            particle.x = SimulationFunctions.x(particle.x, particle.v, particle.a, self.t)
            particle.v = SimulationFunctions.dx(particle.x, particle.v, particle.a, self.t)

        end = timer()

        self.updateTiming = end - start
        self.t += self.timestep

    def getRunningTime(self):
        return self.t
