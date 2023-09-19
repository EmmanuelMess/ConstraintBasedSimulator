#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP

#include <vector>

namespace simulator {
struct SimulationState {
    struct ParticlePosition {
        double x;
        double y;
    };

    std::vector<ParticlePosition> particlePositions;
};
} // simulator

#endif// CONSTRAINTBASEDSIMULATOR_SIMULATIONSTATE_HPP
