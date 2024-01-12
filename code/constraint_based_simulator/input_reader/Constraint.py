from dataclasses import dataclass

from constraint_based_simulator.input_reader.ast.ConstraintProperty import ConstraintProperty
from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType


@dataclass
class Constraint:
    constraintType: ConstraintType
    properties: ConstraintProperty
