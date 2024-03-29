from enum import Enum


class ConstraintOperator(Enum):  # pylint: disable=missing-class-docstring
    EQUAL = 0
    GREATER = 1
    LESS = 2
    LESS_OR_EQUAL = 3
    GREATER_OR_EQUAL = 3
