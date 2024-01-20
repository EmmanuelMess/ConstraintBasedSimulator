from dataclasses import dataclass

from constraint_based_simulator.grapher.drawables.Drawable import Drawable


@dataclass
class BarDrawable(Drawable):
    xStart: int
    yStart: int
    xEnd: int
    yEnd: int
