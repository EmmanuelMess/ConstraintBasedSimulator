#include <optional>

#include <filesystem>

#include <spdlog/spdlog.h>

// This file will be generated automatically when cur_you run the CMake
// configuration step. It creates a namespace called `ConstraintBasedSimulator`. You can modify
// the source template at `configured_files/config.hpp.in`.
#include <internal_use_only/config.hpp>

#include "main_app/input_reader/ReadInput.hpp"

// NOLINTNEXTLINE(bugprone-exception-escape)
int main() {
    try {
        const auto path = std::filesystem::path("/fast/emmanuel/Projects/GitHub/ConstraintBasedSimulator/examples/example1.simulation");
        input_reader::ReadInput inputReader;
        const bool result = inputReader.readFile(path);
        if(!result) {
            spdlog::error("Failed to load file!");
        }

        spdlog::info("Dynamic:");
        for(const auto& point : inputReader.getDynamicPoints()) {
            spdlog::info("{} = ({}, {})", point.name, point.x, point.y);
        }
        spdlog::info("Static:");
        for(const auto& point : inputReader.getStaticPoints()) {
            spdlog::info("{} = ({}, {})", point.name, point.x, point.y);
        }
    } catch (const std::exception &e) { spdlog::error("Unhandled exception in main: {}", e.what()); }
}
