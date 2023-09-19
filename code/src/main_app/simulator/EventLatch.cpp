#include "main_app/simulator/EventLatch.hpp"
#include "main_app/simulator/Simulator.hpp"
#include "main_app/events_manager/EventManager.hpp"

namespace simulator {
void EventLatch::eventLatch() {
    static Simulator simulator;

    simulator.initialize();

    events_manager::EventManager::getInstance().signalStep.connect([](std::chrono::milliseconds) { return simulator.step(); });
}
} // simulator