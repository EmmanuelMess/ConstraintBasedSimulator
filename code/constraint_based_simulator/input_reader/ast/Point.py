from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.Coordinate import Coordinate
from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class Point:  # pylint: disable=missing-class-docstring
    x: Coordinate
    y: Coordinate
    identifier: Identifier

    def __hash__(self):
        return hash(self.identifier)
