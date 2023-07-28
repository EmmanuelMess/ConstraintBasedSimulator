#include <catch2/catch_test_macros.hpp>

#include "main_app/input_reader/ReadInput.hpp"

TEST_CASE("Input Reader", "[example 0]") {
    const std::string path = "/home/emmanuel/Rápido/Projects/GitHub/ConstraintBasedSimulator/examples0.simulator";

    input_reader::ReadInput inputReader;
    inputReader.readFile(path);
}

TEST_CASE("Input Reader", "[example 1]") {
    const std::string path = "/home/emmanuel/Rápido/Projects/GitHub/ConstraintBasedSimulator/examples1.simulator";

    input_reader::ReadInput inputReader;
    inputReader.readFile(path);
}

TEST_CASE("Input Reader", "[example 2]") {
    const std::string path = "/home/emmanuel/Rápido/Projects/GitHub/ConstraintBasedSimulator/examples2.simulator";

    input_reader::ReadInput inputReader;
    inputReader.readFile(path);
}

TEST_CASE("Input Reader", "[example 3]") {
    const std::string path = "/home/emmanuel/Rápido/Projects/GitHub/ConstraintBasedSimulator/examples3.simulator";

    input_reader::ReadInput inputReader;
    inputReader.readFile(path);
}
