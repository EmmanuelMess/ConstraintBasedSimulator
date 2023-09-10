#ifndef CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP
#define CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP

#include "Signal.hpp"

class EventManager {
public:
    static EventManager& getInstance() {
        static EventManager instance;
        return instance;
    }

    EventManager(EventManager&) = delete;
    void operator=(EventManager&) = delete;

    /**
     * Pause UI element activated
     */
    Signal<void()> signalPause;

    /**
     * Set speed UI element activated
     */
    Signal<void()> signalSetSpeed;

    /**
     * Refresh UI element activated
     */
    Signal<void()> signalRefresh;

    /**
     * A new frame is required
     */
    Signal<void()> signalRequireFrame;

    /**
     * A simulation state is required
     */
    Signal<void()> signalRequireState;

private:
    EventManager() = default;
};

#endif// CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP
