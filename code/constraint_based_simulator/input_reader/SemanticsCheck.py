from typing_extensions import List

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
from constraint_based_simulator.input_reader.ast.Constraint import Constraint
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.Statements import Statements
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


def _checkRegistered(registeredIdentifiers: List[Identifier], identifier: Identifier):
    isNotRegistered = identifier not in registeredIdentifiers
    if isNotRegistered:
        MAIN_LOGGER.error(f"Identifier {identifier} is not registered")
    return not isNotRegistered


def checkSemantics(ast: Statements) -> bool:  # noqa: C901
    """
    Validate that a set of statements represents a correctly formed simulation
    :param ast: list of statements, in order, to check
    :return: True if it is a valid simulation state
    """

    registeredIdentifiers: List[Identifier] = []

    for statement in ast:
        if isinstance(statement, Point):
            if _checkRegistered(registeredIdentifiers, statement.identifier):
                return False

            registeredIdentifiers.append(statement.identifier)
        elif isinstance(statement, StaticQualifier):
            if not _checkRegistered(registeredIdentifiers, statement.identifier):
                return False
        elif isinstance(statement, Constraint):
            if not _checkRegistered(registeredIdentifiers, statement.identifierA):
                return False
            if not _checkRegistered(registeredIdentifiers, statement.identifierB):
                return False
            if statement.identifierA == statement.identifierB:
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
