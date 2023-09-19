#pragma once

#include <chrono>

#include "main_app/events_manager/Signal.hpp"
#include "main_app/simulator/SimulationState.hpp"

namespace events_manager {
class EventManager {
public:
    static EventManager &getInstance() {
        static EventManager instance;
        return instance;
    }

    EventManager(EventManager &) = delete;
    void operator=(EventManager &) = delete;

    /**
     * Pause UI element activated
     */
    Signal<void(bool isPaused)> signalPause;

    /**
     * Set speed UI element activated
     */
    Signal<void(unsigned int speed)> signalSetSpeed;

    /**
     * Refresh UI element activated
     */
    Signal<void(std::chrono::milliseconds deltaTime)> signalRefresh;

    /**
     * Step simulation
     */
    Signal<void(std::chrono::milliseconds deltaTime)> signalStep;

    /**
     * A new frame is required
     */
    Signal<void()> signalRequestFrame;

    /**
     * A simulation state was generated
     */
    Signal<void(simulator::SimulationState)> signalSimulationResult;

    /**
     * A new frame has been created
     */
    Signal<void(simulator::SimulationState)> signalNewFrame;

private:
    EventManager() = default;
};
} // events_manager
