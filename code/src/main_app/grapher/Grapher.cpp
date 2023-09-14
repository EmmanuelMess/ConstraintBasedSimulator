#include "main_app/grapher/Grapher.hpp"

#include <chrono>

#include "main_app/grapher/EventManager.hpp"

namespace grapher {

Grapher::Grapher() {
}

void Grapher::onSetSpeed(unsigned int newSpeed) {
    speed = newSpeed;
}

void Grapher::onPause(bool pause) {
    this->paused = pause;
}

void Grapher::onRefresh() {

}

void Grapher::onRequestFrame() {

}

} // grapher