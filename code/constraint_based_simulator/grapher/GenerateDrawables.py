import numpy as np
from typing_extensions import List

from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable
from constraint_based_simulator.simulator.Particle import Particle


def generateDrawableScene(particles: List[Particle]) -> DrawableScene:
    drawableScene = DrawableScene([])

    for particle in particles:
        x: np.ndarray = np.round(particle.x)
        drawableScene.allDrawables.append(PointDrawable(x[0].item(), x[1].item()))

    return drawableScene
