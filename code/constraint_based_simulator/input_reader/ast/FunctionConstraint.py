from dataclasses import dataclass

from typing_extensions import Any

from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType
from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class FunctionConstraint:
    constraintType: ConstraintType
    identifierA: Identifier
    identifierB: Identifier
    function: Any
