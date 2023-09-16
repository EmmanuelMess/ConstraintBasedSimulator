#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP

#include <chrono>
#include <vector>
#include <unordered_map>

#include "Constraint.hpp"
#include "Particle.hpp"
#include "SimulationState.hpp"

namespace simulator {
class Simulator {
public:
    void initialize();
    void step(std::chrono::milliseconds deltaTime);
    [[nodiscard]] SimulationState getCurrentState() const;

private:
    static constexpr float STATIC_POINT_MASS = std::numeric_limits<float>::infinity();
    static constexpr float DYNAMIC_POINT_MASS = std::numeric_limits<float>::epsilon();

    std::vector<Particle> particles;
    std::unordered_map<ParticleId, Constraint> constraints;

    void resetForces();
    void calculateForces(std::chrono::milliseconds deltaTime);
    void calculateConstraintForces();
    SimulationState onRequestState() const;
};
}

#endif// CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP
