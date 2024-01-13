from typing import List

from constraint_based_simulator.input_reader import SemanticsCheck, Parser
from constraint_based_simulator.input_reader.ast.AstTransformer import AstTransformer
from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.Constraint import Constraint
from constraint_based_simulator.input_reader.ast.FunctionConstraint import FunctionConstraint
from constraint_based_simulator.input_reader.ast.GraphicalElement import GraphicalElement
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


class SimulationFile:
    """
    A sort of RAII reader that first parses the simulation file provided and provides all processed data needed from the
    file.
    """

    def __init__(self, path: str):
        rawTree = Parser.readFile(path)
        ast = AstTransformer(visit_tokens=True).transform(rawTree)
        self.semanticsValid = SemanticsCheck.checkSemantics(ast)

        if not self.semanticsValid:
            return

        self.allPoints: List[Point] = [value for value in ast if isinstance(value, Point)]
        self.allPointsByIdentifier: dict[Identifier, Point] = {value.identifier: value for value in self.allPoints}
        self.staticIdentifiers: List[Identifier] = [
            value.identifier for value in ast if isinstance(value, StaticQualifier)
        ]

        self.staticPoints: List[Point] = [
            point for point in self.allPoints if point.identifier in self.staticIdentifiers
        ]

        self.dynamicPoints: List[Point] = [
            point for point in self.allPoints if point.identifier not in self.staticIdentifiers
        ]

        self.allConstraints: List[Constraint] = [
            value for value in ast if isinstance(value, ConstantConstraint) or isinstance(value, FunctionConstraint)
            # HACK because mypy doesnt support unions in isinstance see https://github.com/python/mypy/issues/16358
        ]
        self.constraintsByPoints: dict[Point, Constraint] = {}

        for constraint in self.allConstraints:
            self.constraintsByPoints[self.allPointsByIdentifier[constraint.identifierA]] = constraint
            self.constraintsByPoints[self.allPointsByIdentifier[constraint.identifierB]] = constraint

    def getStaticPoints(self) -> List[Point] | None:
        if not self.semanticsValid:
            return None

        return self.staticPoints

    def getDynamicPoints(self) -> List[Point] | None:
        if not self.semanticsValid:
            return None

        return self.dynamicPoints

    def getConstraints(self) -> dict[Point, Constraint] | None:
        if not self.semanticsValid:
            return None

        return self.constraintsByPoints

    def getGraphics(self) -> dict[Point, GraphicalElement] | None:
        if not self.semanticsValid:
            return None

        return {}
