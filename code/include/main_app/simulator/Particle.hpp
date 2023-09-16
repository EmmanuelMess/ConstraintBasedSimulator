#ifndef CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP
#define CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP

#include "main_app/simulator/ParticleId.hpp"
#include "main_app/simulator/Vector2d.hpp"

namespace simulator {
struct Particle {
    Vector2d position;
    Vector2d force;
    float mass;
    ParticleId identifier;
};
}

#endif// CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP
