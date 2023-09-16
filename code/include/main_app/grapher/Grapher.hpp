#ifndef CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
#define CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP

#include <chrono>

#include "main_app/simulator/Simulator.hpp"

namespace grapher {

class Grapher {
public:
    Grapher();

private:
    bool paused;
    unsigned int speed;
    simulator::Simulator simulation;

    void onSetSpeed(unsigned int newSpeed);

    void onPause(bool pause);

    void onRefresh();

    simulator::SimulationState onRequestFrame() const;
};

} // grapher
#endif// CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
