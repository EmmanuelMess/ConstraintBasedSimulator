#include "main_app/simulator/StateLoader.hpp"

#include <filesystem>

#include <spdlog/spdlog.h>

#include "main_app/input_reader/ReadInput.hpp"

namespace simulator {
input_reader::ReadInput StateLoader::getLoaded() {
    const auto path = std::filesystem::path("/fast/emmanuel/Projects/GitHub/ConstraintBasedSimulator/examples/example1.simulation");
    input_reader::ReadInput inputReader;
    const bool result = inputReader.readFile(path);
    if(!result) {
        spdlog::error("Failed to load file!");
    }

    spdlog::info("Dynamic:");
    for(const auto& point : inputReader.getDynamicPoints()) {
        spdlog::info("{} = ({}, {})", point.identifier, point.x, point.y);
    }
    spdlog::info("Static:");
    for(const auto& point : inputReader.getStaticPoints()) {
        spdlog::info("{} = ({}, {})", point.identifier, point.x, point.y);
    }

    return inputReader;
}
}