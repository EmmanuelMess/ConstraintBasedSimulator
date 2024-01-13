from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class Bar:  # pylint: disable=missing-class-docstring
    start: Identifier
    end: Identifier
