#include "main_app/grapher/Grapher.hpp"

#include <chrono>

#include "main_app/grapher/EventManager.hpp"

namespace grapher {

Grapher::Grapher()
  : paused(true)
  , speed(1) {
    events::EventManager::getInstance().signalSetSpeed.connect([this](unsigned int newSpeed) { onSetSpeed(newSpeed); });
    events::EventManager::getInstance().signalPause.connect([this](bool isPaused) { onPause(isPaused); });
    events::EventManager::getInstance().signalRefresh.connect([this](std::chrono::milliseconds deltaTime) { onRefresh(deltaTime); });
    events::EventManager::getInstance().signalRequestFrame.connect([this]() { onRequestFrame(); });
}

void Grapher::onSetSpeed(unsigned int newSpeed) {
    speed = newSpeed;
}

void Grapher::onPause(bool pause) {
    this->paused = pause;
}

void Grapher::onRefresh(std::chrono::milliseconds deltaTime) {

}

void Grapher::onRequestFrame() {

}

} // grapher