#include "main_app/simulator/Particle.hpp"

#include <utility>

namespace simulator {
Particle::Particle(ParticleId identifier, Vector2d position, bool isStatic)
    : identifier(std::move(identifier))
    , position(std::move(position))
    , velocity(Vector2d::Zero())
    , acceleration(Vector2d::Zero())
    , isStatic(isStatic) {}

} // simulator
