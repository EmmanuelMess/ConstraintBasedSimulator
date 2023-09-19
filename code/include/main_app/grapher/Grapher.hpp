#ifndef CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
#define CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP

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

    void onRefresh() const;

    static void onSimulationResult(const simulator::SimulationState& state);

    /**
     * This is so that events_manager can be registered to call private class memebers
     */
    friend class EventLatch;
};

} // grapher
#endif// CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
