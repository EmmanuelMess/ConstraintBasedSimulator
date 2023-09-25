#include "main_app/grapher/Grapher.hpp"
#include "main_app/events_manager/EventManager.hpp"

#include <chrono>

namespace grapher {

Grapher::Grapher()
  : paused(false)
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
    events_manager::EventManager::getInstance().signalNewFrame(convert(state));
}

grapher::DrawableSimulation Grapher::convert(const simulator::SimulationState& state) {
    grapher::DrawableSimulation drawable = {};
    double maxX = 0.0;
    double maxY = 0.0;

    for(const auto& position : state.particlePositions) {
        if(maxX < position.x) {
            maxX = position.x;
        }

        if(maxY < position.y) {
            maxY = position.y;
        }
    }

    for(const auto& position : state.particlePositions) {
        const double newPositionX = maxX > 0? position.x / maxX : 0.0;
        const double newPositionY = maxY > 0? position.y / maxY : 0.0;

        drawable.particlePositions.emplace_back(newPositionX, newPositionY);
    }

    return drawable;
}

} // grapher