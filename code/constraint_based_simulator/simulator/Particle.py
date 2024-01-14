import numpy as np

from constraint_based_simulator.simulator.IndexedElement import IndexedElement


class Particle(IndexedElement):
    x: np.ndarray
    v: np.ndarray
    a: np.ndarray
    aApplied: np.ndarray
    aConstraint: np.ndarray
    static: bool

    def __init__(self, x: np.ndarray, static: bool = False):
        super(IndexedElement).__init__()
        self.x = x
        self.static = static
        self.v = np.zeros_like(x)
        self.a = np.zeros_like(x)
        self.aApplied = np.zeros_like(x)
        self.aConstraint = np.zeros_like(x)