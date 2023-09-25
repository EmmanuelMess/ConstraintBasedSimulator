#pragma once

#include <vector>

namespace grapher {
struct DrawableSimulation {
    struct ParticlePosition {
        double x;
        double y;
    };

    std::vector<ParticlePosition> particlePositions;
};
}