from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.Coordinate import Coordinate
from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class Point:
    x: Coordinate
    y: Coordinate
    name: Identifier