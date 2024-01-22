from typing_extensions import List

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.FunctionConstraint import FunctionConstraint
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.Statements import Statements
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


def _checkRegistered(registeredIdentifiers: List[Identifier], identifier: Identifier):
    isNotRegistered = identifier not in registeredIdentifiers
    if isNotRegistered:
        MAIN_LOGGER.error(f"Identifier {identifier} is not registered")
    return not isNotRegistered


def checkSemantics(ast: Statements) -> bool:  # noqa: C901 pylint: disable=too-many-branches
    """
    Validate that a set of statements represents a correctly formed simulation
    :param ast: list of statements, in order, to check
    :return: True if it is a valid simulation state
    """

    registeredIdentifiers: List[Identifier] = []

    for statement in ast:
        if isinstance(statement, Point):
            if statement.identifier in registeredIdentifiers:
                MAIN_LOGGER.error(f"Identifier {statement.identifier} already registered")
                return False

            registeredIdentifiers.append(statement.identifier)
        elif isinstance(statement, StaticQualifier):
            if not _checkRegistered(registeredIdentifiers, statement.identifier):
                return False
        elif isinstance(statement, ConstantConstraint):
            if not _checkRegistered(registeredIdentifiers, statement.identifierA):
                return False
            if not _checkRegistered(registeredIdentifiers, statement.identifierB):
                return False
            if statement.identifierA == statement.identifierB:
                MAIN_LOGGER.error(f"Constraint acts on point {statement.identifierA} twice")
                return False
        elif isinstance(statement, FunctionConstraint):
            if not _checkRegistered(registeredIdentifiers, statement.identifierA):
                return False
            if not _checkRegistered(registeredIdentifiers, statement.identifierB):
                return False
            if statement.identifierA == statement.identifierB:
                MAIN_LOGGER.error(f"Constraint acts on point {statement.identifierA} twice")
                return False
        elif isinstance(statement, Bar):
            if not _checkRegistered(registeredIdentifiers, statement.start):
                return False
            if not _checkRegistered(registeredIdentifiers, statement.end):
                return False
        elif isinstance(statement, Circle):
            if not _checkRegistered(registeredIdentifiers, statement.center):
                return False

    return True
