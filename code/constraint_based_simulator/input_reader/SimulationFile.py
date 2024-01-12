from typing import List

from lark import Visitor

from constraint_based_simulator.input_reader.ast.AstTransformer import AstTransformer
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.input_reader.Parser import Parser
from constraint_based_simulator.input_reader.ast.Point import Point


class SimulationFile:
    """
    A sort of RAII reader that first parses the simulation file provided and provides all processed data needed from the
    file.
    """

    def __init__(self, path: str):
        rawTree = Parser.readFile(path)
        ast = AstTransformer(visit_tokens=True).transform(rawTree)

        print(ast)

        #FindStatic().visit(ast)

    def getStaticPoints(self) -> List[Point]:
        return self.staticPoints

    def getDynamicPoints(self) -> List[Point]:
        return self.dynamicPoints

