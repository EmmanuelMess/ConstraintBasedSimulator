import numpy as np
from typing_extensions import List

from constraint_based_simulator.grapher import GenerateDrawables
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable
from constraint_based_simulator.simulator.Particle import Particle


class TestGenerateDrawables:  # pylint: disable=missing-class-docstring
    def testGenerateDrawableScene(self) -> None:  # pylint: disable=missing-function-docstring
        particles: List[Particle] = [
            Particle(np.array([3.4, 4.6])),
            Particle(np.array([55, 34.4]), static=False),
            Particle(np.array([53, 27.5]), static=True),
        ]

        drawableScene = GenerateDrawables.generateDrawableScene(particles)

        assert PointDrawable(3, 5) in drawableScene.allDrawables
        assert PointDrawable(55, 34) in drawableScene.allDrawables
        assert PointDrawable(53, 28) in drawableScene.allDrawables
