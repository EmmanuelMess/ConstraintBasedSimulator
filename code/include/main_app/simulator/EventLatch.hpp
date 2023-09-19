#ifndef CONSTRAINTBASEDSIMULATOR_EVENTLATCH_HPP
#define CONSTRAINTBASEDSIMULATOR_EVENTLATCH_HPP

namespace simulator {
/**
 * This is a sort of "event to register event callbacks" or "initial event"
 * Registers everything that the Grapher needs for callbacks from the EventsManager
 */
class EventLatch {
public:
    static void eventLatch();
};
} // simulator

#endif// CONSTRAINTBASEDSIMULATOR_EVENTLATCH_HPP
