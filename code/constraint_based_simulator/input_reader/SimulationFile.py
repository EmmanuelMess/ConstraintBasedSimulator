from __future__ import annotations

from typing import List

from constraint_based_simulator.input_reader import SemanticsCheck, Parser
from constraint_based_simulator.input_reader.ast.AstTransformer import AstTransformer
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
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

    def __init__(self, path: str) -> None:
        rawTree = Parser.readFile(path)
        ast = AstTransformer(visit_tokens=True).transform(rawTree)
        self.semanticsValid = SemanticsCheck.checkSemantics(ast)

        if not self.semanticsValid:
            return

        allPoints: List[Point] = [value for value in ast if isinstance(value, Point)]
        self.staticIdentifiers: List[Identifier] = [
            value.identifier for value in ast if isinstance(value, StaticQualifier)
        ]

        self.staticPoints: List[Point] = [
            point for point in allPoints if point.identifier in self.staticIdentifiers
        ]

        self.dynamicPoints: List[Point] = [
            point for point in allPoints if point.identifier not in self.staticIdentifiers
        ]

        allConstraints: List[Constraint] = [
            # pylint: disable-next=consider-merging-isinstance
            value for value in ast if isinstance(value, ConstantConstraint) or isinstance(value, FunctionConstraint)
            # HACK because mypy doesn't support unions in isinstance see https://github.com/python/mypy/issues/16358
        ]
        self.constraintsByPoints: dict[Identifier, Constraint] = {}

        for constraint in allConstraints:
            self.constraintsByPoints[constraint.identifierA] = constraint
            self.constraintsByPoints[constraint.identifierB] = constraint

        self.graphics: List[GraphicalElement] = [
            # pylint: disable-next=consider-merging-isinstance
            value for value in ast if isinstance(value, Bar) or isinstance(value, Circle)
            # HACK because mypy doesn't support unions in isinstance see https://github.com/python/mypy/issues/16358
        ]

    def loadedCorrectly(self) -> bool:
        """
        :return: If the file was loaded correctly, it ensures that all methods will work
        """
        return self.semanticsValid

    def getStaticPoints(self) -> List[Point] | None:
        """
        Get static points in file
        :return: if the file does not pass the SemanticsCheck.checkSemantics validation, returns None, otherwise
        a list of AST Point
        """
        if not self.semanticsValid:
            return None

        return self.staticPoints

    def getDynamicPoints(self) -> List[Point] | None:
        """
        Get dynamic points in file
        :return: if the file does not pass the SemanticsCheck.checkSemantics validation, returns None, otherwise
        a list of AST Point
        """
        if not self.semanticsValid:
            return None

        return self.dynamicPoints

    def getConstraints(self) -> dict[Identifier, Constraint] | None:
        """
        Get constraints in file indexed by the point identifier it acts on
        :return: if the file does not pass the SemanticsCheck.checkSemantics validation, returns None, otherwise
        a dictionary of AST Point to Constraint
        """
        if not self.semanticsValid:
            return None

        return self.constraintsByPoints

    def getGraphics(self) -> List[GraphicalElement] | None:
        """
        Get graphical elements in file indexed by the point identifier it latches to
        :return: if the file does not pass the SemanticsCheck.checkSemantics validation, returns None, otherwise
        a dictionary of AST Points to GraphicalElement
        """
        if not self.semanticsValid:
            return None

        return self.graphics
