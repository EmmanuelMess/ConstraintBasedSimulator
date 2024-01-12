from dataclasses import dataclass


@dataclass
class Constraint:
    constraintType: ConstraintType
    properties: ConstraintProperty