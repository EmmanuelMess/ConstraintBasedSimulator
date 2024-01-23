from __future__ import annotations

from lark import Transformer, Token
from typing_extensions import List, Any, Tuple

from constraint_based_simulator.common import MainLogger
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.ConstraintOperator import ConstraintOperator
from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType
from constraint_based_simulator.input_reader.ast.Coordinate import Coordinate
from constraint_based_simulator.input_reader.ast.FunctionConstraint import FunctionConstraint
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.Statement import Statement
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


class AstTransformer(Transformer):
    """
    Takes the Tree from lark and transforms into a list of Statements typed with custom ast types
    """

    def start(self, value: List[Statement]) -> List[Statement]:  # pylint: disable=missing-function-docstring
        return value

    def point_definition(self, tokens: Tuple[Identifier, Coordinate, Coordinate])\
            -> Point:  # pylint: disable=missing-function-docstring
        return Point(tokens[1], tokens[2], tokens[0])

    def static_qualifier(self, tokens: Tuple[Identifier])\
            -> StaticQualifier:  # pylint: disable=missing-function-docstring
        return StaticQualifier(tokens[0])

    def constant_constraint(self, tokens: Tuple[ConstraintType, Identifier, Identifier, ConstraintOperator, float])\
            -> ConstantConstraint:  # pylint: disable=missing-function-docstring
        return ConstantConstraint(*tokens)

    def function_constraint(self, tokens: Tuple[ConstraintType, Identifier, Identifier, Any])\
            -> FunctionConstraint:  # pylint: disable=missing-function-docstring
        return FunctionConstraint(*tokens)

    def circle(self, values: Tuple[Identifier, float]) -> Circle:  # pylint: disable=missing-function-docstring
        return Circle(values[0], values[1])

    def bar(self, value: Tuple[Identifier, Identifier])\
            -> Bar:  # pylint: disable=missing-function-docstring,disallowed-name
        return Bar(value[0], value[1])

    def CONSTRAINT_TYPE(self, constraintType: str)\
            -> ConstraintType | None:  # pylint: disable=missing-function-docstring
        switch = {
            "distance": ConstraintType.DISTANCE,
            "force": ConstraintType.FORCE
        }

        if constraintType not in switch:
            MainLogger.MAIN_LOGGER.error(f"Forgot to add a constraint type \"{constraintType}\" to the AST")
            return None

        return switch[constraintType]  # HACK for retrocompatibility with 3.8 (still supported)
        # see https://stackoverflow.com/a/11479840/3124150

    def CONSTRAINT_OPERATOR(self, op: str) -> ConstraintOperator | None:  # pylint: disable=missing-function-docstring
        switch = {
            "==": ConstraintOperator.EQUAL,
            "<": ConstraintOperator.GREATER,
            ">": ConstraintOperator.LESS,
            ">=": ConstraintOperator.LESS_OR_EQUAL,
            "<=": ConstraintOperator.GREATER_OR_EQUAL,
        }

        # HACK there is a bug in pylint see https://github.com/pylint-dev/pylint/issues/9360
        # pylint: disable-next=consider-iterating-dictionary
        if op not in switch.keys():
            MainLogger.MAIN_LOGGER.error(f"Forgot to add an operator type \"{op}\" to the AST")
            return None

        return switch[op]  # HACK for retrocompatibility with 3.8 (still supported)
        # see https://stackoverflow.com/a/11479840/3124150

    def IDENTIFIER(self, token: Token) -> Identifier:  # pylint: disable=missing-function-docstring
        return token.value

    def DECIMAL(self, token: Token) -> Coordinate:  # pylint: disable=missing-function-docstring
        return float(token.value)
