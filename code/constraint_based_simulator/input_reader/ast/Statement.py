from typing import Union

from constraint_based_simulator.input_reader.ast.Constraint import Constraint
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


Statement = Union[Point, StaticQualifier, Constraint]
