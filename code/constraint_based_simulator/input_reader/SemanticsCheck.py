from typing_extensions import List

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
from constraint_based_simulator.input_reader.ast.Constraint import Constraint
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.Statements import Statements
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


def checkSemantics(ast: Statements) -> bool:
    registeredIdentifiers: List[Identifier] = []

    def checkRegistered(identifier: Identifier):
        isNotRegistered = identifier not in registeredIdentifiers
        if isNotRegistered:
            MAIN_LOGGER.error(f"Identifier {identifier} is not registered")
        return not isNotRegistered

    for statement in ast:
        if isinstance(statement, Point):
            if checkRegistered(statement.identifier):
                return False

            registeredIdentifiers.append(statement.identifier)
        elif isinstance(statement, StaticQualifier):
            if not checkRegistered(statement.identifier):
                return False
        elif isinstance(statement, Constraint):
            if not checkRegistered(statement.identifierA):
                return False
            if not checkRegistered(statement.identifierB):
                return False
            if statement.identifierA == statement.identifierB:
                return False
        elif isinstance(statement, Bar):
            if not checkRegistered(statement.start):
                return False
            if not checkRegistered(statement.end):
                return False
        elif isinstance(statement, Circle):
            if not checkRegistered(statement.center):
                return False

    return True


