#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP

#include "main_app/simulator/Particle.hpp"
#include "main_app/simulator/Constraint.hpp"

namespace simulator {
struct SimulationState {
    std::vector<Particle> particles;
    std::unordered_map<ParticleId, Constraint> constraints;
};
} // simulator

#endif// CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP
