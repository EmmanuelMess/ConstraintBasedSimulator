#pragma once

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
    std::vector<std::shared_ptr<Particle>> particles;
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
