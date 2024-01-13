from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.ConstraintOperator import ConstraintOperator
from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType
from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class ConstantConstraint:  # pylint: disable=missing-class-docstring
    constraintType: ConstraintType
    identifierA: Identifier
    identifierB: Identifier
    operator: ConstraintOperator
    distance: float
