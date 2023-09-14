#ifndef CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP
#define CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP

#include "Signal.hpp"

namespace events {
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
     * A new frame is required
     */
    Signal<void()> signalRequestFrame;

    /**
     * A simulation state is required
     */
    Signal<simulator::SimulationState()> signalRequestState;

    /**
     * A new frame has been created
     */
    Signal<void()> signalNewFrame;

private:
    EventManager() = default;
};
} // events

#endif// CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP
