#pragma once

#include "DrawableSimulation.hpp"
#include "main_app/simulator/SimulationState.hpp"
#include <chrono>

namespace grapher {

class EventLatch;

class Grapher {
public:
    Grapher();

private:
    bool paused;
    unsigned int speed;

    void onSetSpeed(unsigned int newSpeed);

    void onPause(bool pause);

    void onRefresh(std::chrono::milliseconds step) const;

    static void onSimulationResult(const simulator::SimulationState& state);

    static grapher::DrawableSimulation convert(const simulator::SimulationState& state);

    /**
     * This is so that events_manager can be registered to call private class memebers
     */
    friend class EventLatch;
};

} // grapher
