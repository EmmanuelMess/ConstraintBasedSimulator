from dataclasses import dataclass

import numpy as np

from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.simulator.IndexedElement import IndexedElement


@dataclass
class Particle(IndexedElement):  # pylint: disable=missing-class-docstring,too-few-public-methods
    x: np.ndarray
    v: np.ndarray
    a: np.ndarray
    aApplied: np.ndarray
    aConstraint: np.ndarray
    static: bool
    identifier: Identifier
    """
    This identifier is used to keep track of the point in the grapher
    """

    def __init__(self, x: np.ndarray, identifier: Identifier, static: bool = False):
        self.x = x
        self.static = static
        self.v = np.zeros_like(x)
        self.a = np.zeros_like(x)
        self.aApplied = np.zeros_like(x)
        self.aConstraint = np.zeros_like(x)
        self.identifier = identifier
