import numpy as np
from typing_extensions import List

from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.Simulation import Simulation
from constraint_based_simulator.simulator.constraints.CircleConstraint import CircleConstraint
from constraint_based_simulator.simulator.constraints.Constraint import Constraint
from constraint_based_simulator.simulator.constraints.DistanceConstraint import DistanceConstraint


class TestSimulation:  # pylint: disable=missing-class-docstring

    def testCircleConstraintSingleParticle(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([
            Particle(np.array([25, 0], dtype=np.float64), "A")
        ])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            CircleConstraint(particles[0], np.array([50, 20], dtype=np.float64), np.float64(100))
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0]], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testDistanceConstraintSingleParticle(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([
            Particle(np.array([50, 25], dtype=np.float64), "A"),
            Particle(np.array([50, 50], dtype=np.float64), "B"),
            Particle(np.array([25, 0], dtype=np.float64), "C"),
            Particle(np.array([0, 0], dtype=np.float64), "D"),
        ])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            DistanceConstraint(particles[0], particles[1], np.float64(100)),
            DistanceConstraint(particles[2], particles[3], np.float64(100)),
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testCircleDistanceConstraintMultiParticles(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([
            Particle(np.array([0, 0], dtype=np.float64), "A"),
            Particle(np.array([25, 25], dtype=np.float64), "B"),
        ])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            CircleConstraint(particles[0], np.array([25, 0], dtype=np.float64), np.float64(100)),
            DistanceConstraint(particles[0], particles[1], np.float64(20)),
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0], [0, 0]], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testDistanceConstraintMultiParticles(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([
            Particle(np.array([0, 0], dtype=np.float64), "A"),
            Particle(np.array([25, -25], dtype=np.float64), "B"),
            Particle(np.array([50, 0], dtype=np.float64), "C"),
            Particle(np.array([75, -25], dtype=np.float64), "D"),
            Particle(np.array([100, 0], dtype=np.float64), "E"),
            Particle(np.array([125, -25], dtype=np.float64), "F"),
            Particle(np.array([150, 0], dtype=np.float64), "G"),
        ])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            DistanceConstraint(particles[0], particles[1], np.float64(25)),
            DistanceConstraint(particles[0], particles[2], np.float64(25)),
            DistanceConstraint(particles[1], particles[2], np.float64(25)),
            DistanceConstraint(particles[1], particles[3], np.float64(25)),
            DistanceConstraint(particles[2], particles[3], np.float64(25)),
            DistanceConstraint(particles[2], particles[4], np.float64(25)),
            DistanceConstraint(particles[3], particles[4], np.float64(25)),
            DistanceConstraint(particles[3], particles[5], np.float64(25)),
            DistanceConstraint(particles[4], particles[5], np.float64(25)),
            DistanceConstraint(particles[4], particles[6], np.float64(25)),
            DistanceConstraint(particles[5], particles[6], np.float64(25)),
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0] for i in range(len(particles))], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testDistanceConstraintsMultiParticle(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([
            Particle(np.array([0, 0], dtype=np.float64), "A", static=True),
            Particle(np.array([25, -25], dtype=np.float64), "B"),
            Particle(np.array([50, 0], dtype=np.float64), "C"),
            Particle(np.array([75, -25], dtype=np.float64), "D"),
            Particle(np.array([100, 0], dtype=np.float64), "E"),
            Particle(np.array([125, -25], dtype=np.float64), "F"),
            Particle(np.array([150, 0], dtype=np.float64), "G", static=True),
        ])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            DistanceConstraint(particles[0], particles[1], np.float64(50)),
            DistanceConstraint(particles[0], particles[2], np.float64(50)),
            DistanceConstraint(particles[1], particles[2], np.float64(50)),
            DistanceConstraint(particles[1], particles[3], np.float64(50)),
            DistanceConstraint(particles[2], particles[3], np.float64(50)),
            DistanceConstraint(particles[2], particles[4], np.float64(50)),
            DistanceConstraint(particles[3], particles[4], np.float64(50)),
            DistanceConstraint(particles[3], particles[5], np.float64(50)),
            DistanceConstraint(particles[4], particles[5], np.float64(50)),
            DistanceConstraint(particles[4], particles[6], np.float64(50)),
            DistanceConstraint(particles[5], particles[6], np.float64(50)),
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0] for i in range(len(particles))], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testCircleSingleParticle(self) -> None:  # pylint: disable=missing-function-docstring
        particles: IndexerIterator[Particle] = IndexerIterator([Particle(np.array([25, 0], dtype=np.float64), "A")])

        constraints: IndexerIterator[Constraint] = IndexerIterator([
            CircleConstraint(particles[0], np.array([50, 20], dtype=np.float64), np.float64(100)),
            CircleConstraint(particles[0], np.array([100, 20], dtype=np.float64), np.float64(100))
        ])

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0]], dtype=np.float64)

        simulator = Simulation(particles, constraints, force, False)
        simulator.update(np.float64(0))

    def testDistanceConstraintsInGrid(self) -> None:  # pylint: disable=missing-function-docstring
        CONSTRAINT_DISTANCE = np.float64(100)
        DISTANCE = 50
        EXTERNAL_GRID_WIDTH = 4
        INTERNAL_GRID_WIDTH = EXTERNAL_GRID_WIDTH-1

        externalGrid = range(0, DISTANCE*EXTERNAL_GRID_WIDTH, DISTANCE)
        internalGrid = range(DISTANCE//2, DISTANCE*INTERNAL_GRID_WIDTH, DISTANCE)
        positionsGridA = [np.array([x, y], dtype=np.float64) for x in externalGrid for y in externalGrid]
        positionsGridB = [np.array([x, y], dtype=np.float64) for x in internalGrid for y in internalGrid]

        particles: List[Particle] = []

        for xy in list(positionsGridA)+list(positionsGridB):
            particles.append(Particle(np.array(xy, dtype=np.float64), "C"))

        constraints: List[Constraint] = []

        M = len(positionsGridA)
        K = EXTERNAL_GRID_WIDTH
        N = INTERNAL_GRID_WIDTH

        for i in range(len(positionsGridB)):
            constraints.append(DistanceConstraint(particles[i+i//N], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+1], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+K], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+K+1], particles[i+M], CONSTRAINT_DISTANCE))

        def force(_: np.float64) -> np.ndarray:
            return np.array([[0, 0] for i in range(len(particles))], dtype=np.float64)

        simulator = Simulation(IndexerIterator[Particle](particles), IndexerIterator[Constraint](constraints),
                               force, False)
        simulator.update(np.float64(0))

    def testDistanceConstraintsInGridWithDiagonals(self) -> None:  # pylint: disable=missing-function-docstring
        DISTANCE = 50
        CONSTRAINT_DISTANCE = np.float64(np.sqrt(DISTANCE**2+DISTANCE**2)/2)
        EXTERNAL_GRID_WIDTH = 4
        INTERNAL_GRID_WIDTH = EXTERNAL_GRID_WIDTH-1

        externalGrid = range(0, DISTANCE*EXTERNAL_GRID_WIDTH, DISTANCE)
        internalGrid = range(DISTANCE//2, DISTANCE*INTERNAL_GRID_WIDTH, DISTANCE)
        positionsGridA = [np.array([x, y], dtype=np.float64) for x in externalGrid for y in externalGrid]
        positionsGridB = [np.array([x, y], dtype=np.float64) for x in internalGrid for y in internalGrid]

        particles: List[Particle] = []

        for xy in list(positionsGridA)+list(positionsGridB):
            particles.append(Particle(np.array(xy, dtype=np.float64), "A"))

        constraints: List[Constraint] = []

        M = len(positionsGridA)
        K = EXTERNAL_GRID_WIDTH
        N = INTERNAL_GRID_WIDTH

        for i in range(len(positionsGridB)):
            constraints.append(DistanceConstraint(particles[i+i//N], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+1], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+K], particles[i+M], CONSTRAINT_DISTANCE))
            constraints.append(DistanceConstraint(particles[i+i//N+K+1], particles[i+M], CONSTRAINT_DISTANCE))

            constraints.append(DistanceConstraint(particles[i+i//N], particles[i+i//N+1], np.float64(DISTANCE)))
            constraints.append(DistanceConstraint(particles[i+i//N+1], particles[i+i//N+K+1], np.float64(DISTANCE)))
            constraints.append(DistanceConstraint(particles[i+i//N+K+1], particles[i+i//N+K], np.float64(DISTANCE)))
            constraints.append(DistanceConstraint(particles[i+i//N+K], particles[i+i//N], np.float64(DISTANCE)))

        def force(t: np.float64) -> np.ndarray:
            return np.array([[10*np.abs(np.sin(1000*t)), -10*np.abs(np.sin(1000*t))]]
                            + [[0, 0] for i in range(len(particles)-1)], dtype=np.float64)

        simulator = Simulation(IndexerIterator[Particle](particles), IndexerIterator[Constraint](constraints), force,
                               False)
        simulator.update(np.float64(0))
