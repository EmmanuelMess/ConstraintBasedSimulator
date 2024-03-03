from dataclasses import dataclass

from constraint_based_simulator.grapher.drawables.Drawable import Drawable
from constraint_based_simulator.input_reader.ast.Identifier import Identifier


@dataclass
class PointDrawable(Drawable):
    x: int
    y: int
    identifier: Identifier
