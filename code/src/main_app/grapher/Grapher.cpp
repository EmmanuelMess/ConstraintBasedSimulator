#include "main_app/grapher/Grapher.hpp"
#include "main_app/events_manager/EventManager.hpp"

#include <chrono>

namespace grapher {

Grapher::Grapher()
  : paused(true)
  , speed(1) {

}

void Grapher::onSetSpeed(unsigned int newSpeed) {
    speed = newSpeed;
}

void Grapher::onPause(bool pause) {
    this->paused = pause;
}

void Grapher::onRefresh() const {
    if(!paused) {
        events_manager::EventManager::getInstance().signalStep(std::chrono::milliseconds(100));
    }
}

void Grapher::onSimulationResult(const simulator::SimulationState& state) {
    events_manager::EventManager::getInstance().signalNewFrame(state);
}

} // grapher