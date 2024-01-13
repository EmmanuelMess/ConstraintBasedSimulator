from typing import Union

from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.FunctionConstraint import FunctionConstraint


Constraint = Union[ConstantConstraint, FunctionConstraint]
