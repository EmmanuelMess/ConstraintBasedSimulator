from dataclasses import dataclass

from constraint_based_simulator.grapher.drawables.Drawable import Drawable


@dataclass
class CircleDrawable(Drawable):
    x: int
    y: int
    radius: int
