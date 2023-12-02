#pragma once

#include "main_app/simulator/ParticleId.hpp"
#include "main_app/simulator/Vector2d.hpp"

namespace simulator {
struct Particle {
    ParticleId identifier;
    Vector2d position;
    Vector2d velocity;
    Vector2d acceleration;
    bool isStatic;

    Particle(ParticleId identifier, Vector2d position, bool isStatic);
};
}
