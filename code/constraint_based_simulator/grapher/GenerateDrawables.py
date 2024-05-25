import numpy as np
from typing_extensions import List, Tuple

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.grapher.drawables.BarDrawable import BarDrawable
from constraint_based_simulator.grapher.drawables.CircleDrawable import CircleDrawable
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable
from constraint_based_simulator.input_reader.ast.Bar import Bar
from constraint_based_simulator.input_reader.ast.Circle import Circle
from constraint_based_simulator.input_reader.ast.GraphicalElement import GraphicalElement
from constraint_based_simulator.input_reader.ast.Identifier import Identifier
from constraint_based_simulator.simulator.NamedParticle import NamedParticle
from simulator.Particle import Particle


def generateDrawableScene(particles: List[NamedParticle], graphicalElements: List[GraphicalElement]) -> DrawableScene:
    drawableScene = DrawableScene([])

    indexedPositions: dict[Identifier, Tuple[int, int]] = \
        {particle.id: particleToPosition(particle.particle) for particle in particles}  # TODO optimize

    for identifier, position in indexedPositions.items():
        drawableScene.allDrawables.append(PointDrawable(position[0], position[1], identifier))

    for element in graphicalElements:
        if isinstance(element, Bar):
            start = indexedPositions[element.start]
            end = indexedPositions[element.end]
            drawableScene.allDrawables.append(BarDrawable(start[0], start[1], end[0], end[1]))
        elif isinstance(element, Circle):
            center = indexedPositions[element.center]
            drawableScene.allDrawables.append(CircleDrawable(center[0], center[1], round(element.length)))
        else:
            MAIN_LOGGER.error(f"GraphicalElement not implemented for simulator {element}")

    return drawableScene


def particleToPosition(particle: Particle) -> Tuple[int, int]:
    position = np.round(particle.x)
    return position[0].item(), position[1].item()
