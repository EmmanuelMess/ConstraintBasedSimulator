#include "main_app/grapher/EventLatch.hpp"

#include "main_app/grapher/Grapher.hpp"
#include "main_app/events_manager/EventManager.hpp"
#include "main_app/simulator/SimulationState.hpp"

namespace grapher {
void EventLatch::eventLatch() {
    static Grapher grapher;

    events_manager::EventManager::getInstance().signalSetSpeed.connect([](unsigned int newSpeed) { grapher.onSetSpeed(newSpeed); });
    events_manager::EventManager::getInstance().signalPause.connect([](bool isPaused) { grapher.onPause(isPaused); });
    events_manager::EventManager::getInstance().signalRefresh.connect([](std::chrono::milliseconds) { grapher.onRefresh(); });
    events_manager::EventManager::getInstance().signalSimulationResult.connect([](const simulator::SimulationState &state) { grapher.onSimulationResult(state); });
}
}
