#include "main_app/events_manager/EventsInitializer.hpp"

#include "main_app/grapher/EventLatch.hpp"
#include "main_app/simulator/EventLatch.hpp"

namespace events_manager {
EventsInitializer::EventsInitializer() {
    grapher::EventLatch::eventLatch();
    simulator::EventLatch::eventLatch();
}
}
