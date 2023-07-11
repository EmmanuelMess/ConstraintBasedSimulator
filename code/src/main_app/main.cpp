#include <optional>

#include <spdlog/spdlog.h>


// This file will be generated automatically when cur_you run the CMake
// configuration step. It creates a namespace called `ConstraintBasedSimulator`. You can modify
// the source template at `configured_files/config.hpp.in`.
#include <internal_use_only/config.hpp>

#include "main_app/input_file.hpp"
#include "main_app/simulation.hpp"

// NOLINTNEXTLINE(bugprone-exception-escape)
int main() {
    try {
        input_reader::test();
        simulation::test();
    } catch (const std::exception &e) { spdlog::error("Unhandled exception in main: {}", e.what()); }
}
