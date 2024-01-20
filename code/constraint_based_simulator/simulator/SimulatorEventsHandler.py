import copy

import numpy as np
from typing_extensions import List, Callable, Tuple

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.common.Singleton import Singleton
from constraint_based_simulator.events_manager import InitializationSignals, GraphingSignals
from constraint_based_simulator.events_manager.EventsHandler import EventsHandler
from constraint_based_simulator.input_reader.SimulationFile import SimulationFile
from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.Constraint import Constraint as AstConstraint
from constraint_based_simulator.input_reader.ast.ConstraintOperator import ConstraintOperator
from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.simulator import SimulationHolder, ParticlesHolder
from constraint_based_simulator.simulator.IndexerIterator import IndexerIterator
from constraint_based_simulator.simulator.Particle import Particle
from constraint_based_simulator.simulator.Simulation import Simulation
from constraint_based_simulator.simulator.SimulationData import SimulationData
from constraint_based_simulator.simulator.constraints.Constraint import Constraint as SimulatorConstraint
from constraint_based_simulator.simulator.constraints.DistanceConstraint import DistanceConstraint


class SimulatorEventsHandler(EventsHandler, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        InitializationSignals.simulationPropertiesAvailable.connect(self.loadSimulator)
        GraphingSignals.signalStep.connect(self.step)

    def loadSimulator(self, simulationFile: SimulationFile):
        ParticlesHolder.particles, pointMapping = SimulatorEventsHandler.convertParticles(
            simulationFile.getStaticPoints(), simulationFile.getDynamicPoints())  # type: ignore

        particles: IndexerIterator[Particle] = ParticlesHolder.particles
        constraints: IndexerIterator[SimulatorConstraint] = SimulatorEventsHandler.convertConstraints(
            pointMapping, simulationFile.getConstraints())
        timestep: np.float64 = np.float64(0.016)
        force: Callable[[np.float64], np.ndarray] = lambda x: np.array([[0, 0] for _ in particles])
        printData: bool = True
        SimulationHolder.simulation = Simulation(particles, constraints, timestep, force, printData)
        InitializationSignals.simulatorLoaded.emit()

    def step(self, currentTime: float):
        if SimulationHolder.simulation is None:
            MAIN_LOGGER.error("Simulation update without simulation loaded!")
            return

        SimulationHolder.simulation.update()

        simulationData = SimulationData(copy.deepcopy(ParticlesHolder.particles))

        GraphingSignals.signalRequestState.emit(simulationData)

    @staticmethod
    def convertParticles(staticPoints: List[Point], dynamicPoints: List[Point]) \
            -> Tuple[IndexerIterator[Particle], dict[Identifier, Particle]]:
        """
        Convert AST points to simulator particles
        """

        mapping: dict[Identifier, Particle] = {}

        mapping |= {staticPoint.identifier: Particle(x=np.array([staticPoint.x, staticPoint.y]), static=True)
                    for staticPoint in staticPoints}
        mapping |= {dynamicPoint.identifier: Particle(x=np.array([dynamicPoint.x, dynamicPoint.y]), static=False)
                    for dynamicPoint in dynamicPoints}

        return IndexerIterator(list(mapping.values())), mapping

    @staticmethod
    def convertConstraints(mapping: dict[Identifier, Particle], constraints: dict[Point, AstConstraint]) \
            -> IndexerIterator[SimulatorConstraint]:
        """
        Convert AST constraints to simulator constraints
        """
        constraintList: List[SimulatorConstraint] = []

        for constraint in constraints.values():
            if isinstance(constraint, ConstantConstraint):
                if constraint.constraintType != ConstraintType.DISTANCE:
                    MAIN_LOGGER.error(f"Constraint type not implemented for simulator {constraint.constraintType}")
                    continue

                if constraint.operator != ConstraintOperator.EQUAL:
                    MAIN_LOGGER.error(f"Constraint operator not implemented for simulator {constraint.operator}")

                distance = np.float64(constraint.distance)
                simulatorConstraint = DistanceConstraint(
                    mapping[constraint.identifierA], mapping[constraint.identifierB], distance
                )
                constraintList.append(simulatorConstraint)
            else:
                MAIN_LOGGER.error(f"Constraint not implemented for simulator: {constraint}")

        return IndexerIterator(constraintList)
