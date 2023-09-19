#pragma once

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
