#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP

#include <chrono>
#include <vector>
#include <unordered_map>

#include "main_app/simulator/Constraint.hpp"
#include "main_app/simulator/Particle.hpp"
#include "main_app/simulator/SimulationState.hpp"

namespace simulator {
class EventLatch;

class Simulator {
public:
    void initialize();
    void step();
    [[nodiscard]] SimulationState getCurrentState() const;

private:
    static constexpr float STATIC_POINT_MASS = std::numeric_limits<float>::infinity();
    static constexpr float DYNAMIC_POINT_MASS = std::numeric_limits<float>::epsilon();

    std::vector<Particle> particles;
    std::unordered_map<ParticleId, Constraint> constraints;

    void resetForces();
    void calculateConstraintForces();
    SimulationState onRequestState() const;

    /**
     * This is so that events_manager can be registered to call private class memebers
     */
    friend class EventLatch;
};
}

#endif// CONSTRAINTBASEDSIMULATOR_SIMULATOR_HPP
