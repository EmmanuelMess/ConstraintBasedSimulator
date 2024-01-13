from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class StaticQualifier:  # pylint: disable=missing-class-docstring
    identifier: Identifier
