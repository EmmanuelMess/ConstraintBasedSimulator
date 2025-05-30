import copy

import numpy as np
from typing_extensions import List, Callable, Tuple, Dict

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
from constraint_based_simulator.simulator.NamedParticle import NamedParticle
from constraint_based_simulator.simulator.SimulationData import SimulationData
from simulator import Indexer
from simulator.Particle import Particle
from simulator.Simulation import Simulation
from simulator.constraints.Constraint import Constraint as SimulatorConstraint
from simulator.constraints.DistanceConstraint import DistanceConstraint


class SimulatorEventsHandler(EventsHandler, metaclass=Singleton):
    """
    Handles all the signals for the simulator module
    """

    def __init__(self) -> None:
        super().__init__()
        InitializationSignals.simulationPropertiesAvailable.connect(self.loadSimulator)
        GraphingSignals.signalStep.connect(self.step)

    def loadSimulator(self, simulationFile: SimulationFile) -> None:
        """
        Load simulation in this module, after this initialization the module can be stepped to run it
        """

        staticPoints = simulationFile.getStaticPoints()
        dynamicPoints = simulationFile.getDynamicPoints()
        constraints = simulationFile.getConstraints()
        if staticPoints is None or dynamicPoints is None or constraints is None:
            MAIN_LOGGER.error("Points or constraints are None")
            return

        particlesIndexed, pointMapping = SimulatorEventsHandler.convertParticles(staticPoints, dynamicPoints)

        ParticlesHolder.particles = [NamedParticle(particle, id) for (id, particle) in pointMapping.items()]

        constraintsIndexed: List[SimulatorConstraint] = (
            SimulatorEventsHandler.convertConstraints(pointMapping, constraints))
        force: Callable[[np.float64], np.ndarray] = lambda x: np.array([[0, 0] for _ in particlesIndexed])
        printData: bool = True
        SimulationHolder.simulation = Simulation(particlesIndexed, constraintsIndexed, force, printData)
        InitializationSignals.simulatorLoaded.emit()

    def step(self, currentTime: float) -> None:
        """
        Run a simulation step
        :param currentTime: The amount of time that passes between steps
        """
        if SimulationHolder.simulation is None:
            MAIN_LOGGER.error("Simulation update without simulation loaded!")
            return

        SimulationHolder.simulation.update(np.float64(currentTime))

        simulationData = SimulationData(copy.deepcopy(ParticlesHolder.particles))

        GraphingSignals.signalRequestState.emit(simulationData)

    @staticmethod
    def convertParticles(staticPoints: List[Point], dynamicPoints: List[Point]) \
            -> Tuple[List[Particle], Dict[Identifier, Particle]]:
        """
        Convert AST points to simulator particles
        """

        staticPointsMapping: Dict[Identifier, Particle] = {
            staticPoint.identifier:
                Particle(np.array([staticPoint.x, staticPoint.y]), static=True)
            for staticPoint in staticPoints
        }
        dynamicPointsMapping: Dict[Identifier, Particle] = {
            dynamicPoint.identifier:
                Particle(np.array([dynamicPoint.x, dynamicPoint.y]), static=False)
            for dynamicPoint in dynamicPoints}

        # Weird merging syntax for Python 3.8
        mapping: Dict[Identifier, Particle] = {**staticPointsMapping, **dynamicPointsMapping}

        return Indexer.indexer(list(mapping.values())), mapping

    @staticmethod
    def convertConstraints(mapping: Dict[Identifier, Particle], constraints: Dict[Identifier, AstConstraint]) \
            -> List[SimulatorConstraint]:
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

        return Indexer.indexer(constraintList)
