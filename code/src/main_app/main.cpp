#include <optional>

#include <spdlog/spdlog.h>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wold-style-cast"
#include <backward.hpp>
#pragma GCC diagnostic pop

#include <csignal>

// This file will be generated automatically when cur_you run the CMake
// configuration step. It creates a namespace called `ConstraintBasedSimulator`. You can modify
// the source template at `configured_files/config.hpp.in`.
#include <internal_use_only/config.hpp>

#include "main_app/events_manager/EventsInitializer.hpp"
#include "main_app/input_reader/ReadInput.hpp"
#include "main_app/ui/UiRunner.hpp"

backward::SignalHandling signalHandling;

// NOLINTNEXTLINE(bugprone-exception-escape)
int main(int argc, char *argv[]) {
    try {
        const events_manager::EventsInitializer eventsInitializer;
        return ui::runUi(argc, argv);
    } catch (const std::exception &e) { spdlog::error("Unhandled exception in main: {}", e.what()); }
}
