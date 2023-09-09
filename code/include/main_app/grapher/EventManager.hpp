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

    Signal<void()> signalPause;
    Signal<void()> signalSetSpeed;
    Signal<void()> signalRefresh;
    Signal<void()> signalRequireFrame;
    Signal<void()> signalRequireState;

private:
    EventManager() = default;
};

#endif// CONSTRAINTBASEDSIMULATOR_EVENTMANAGER_HPP
