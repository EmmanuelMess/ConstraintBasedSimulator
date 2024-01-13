from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class Circle:  # pylint: disable=missing-class-docstring
    center: Identifier
    length: float
