#ifndef CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP
#define CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP

#include <Eigen/Core>

namespace simulator {
struct Particle {
    Eigen::Vector2f position;
    Eigen::Vector2f force;
    float mass;
};
}

#endif// CONSTRAINTBASEDSIMULATOR_PARTICLE_HPP
