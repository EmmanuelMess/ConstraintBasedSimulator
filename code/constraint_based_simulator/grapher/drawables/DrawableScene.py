from dataclasses import dataclass

from typing_extensions import List

from constraint_based_simulator.grapher.drawables.Drawable import Drawable


@dataclass
class DrawableScene:
    allDrawables: List[Drawable]