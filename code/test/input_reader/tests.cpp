#include <catch2/catch_test_macros.hpp>

#include <filesystem>
#include <fstream>

#include "main_app/input_reader/ReadInput.hpp"

TEST_CASE("Read file", "[InputReader::readFile]") {
    SECTION("single point") {
        std::error_code error;
        const std::string path = std::filesystem::temp_directory_path(error) / "example.simulator";
        REQUIRE(error.value() == 0);

        {
            std::ofstream output(path);
            output << "A = (0, 0)\n";
            output.close();
        }

        input_reader::ReadInput inputReader;
        REQUIRE(inputReader.readFile(path));

        const std::vector<input_reader::Point> dynamicPoints = { { .x = 0, .y = 0, .identifier = "A"} };
        REQUIRE(inputReader.getDynamicPoints() == dynamicPoints);

        REQUIRE(inputReader.getStaticPoints().empty());
        REQUIRE(inputReader.getConstraints().empty());
        REQUIRE(inputReader.getGraphics().empty());
    }

    SECTION("multiple points with qualifiers") {
        std::error_code error;
        const std::string path = std::filesystem::temp_directory_path(error) / "example.simulator";
        REQUIRE(error.value() == 0);

        {
            std::ofstream output(path);
            output << "A = (0, 0)\n"
                   << "B = (3.0, -90)\n"
                   << "C = (0.5, 5000)\n"
                   << "D = (200, 800)\n"
                   << "static A\n"
                   << "static D\n";
            output.close();
        }

        input_reader::ReadInput inputReader;
        REQUIRE(inputReader.readFile(path));

        const std::vector<input_reader::Point> staticPoints = {
            { .x = 0, .y = 0, .identifier = "A" }, { .x = 200, .y = 800, .identifier = "D" }
        };
        REQUIRE(inputReader.getStaticPoints() == staticPoints);

        const std::vector<input_reader::Point> dynamicPoints = {
            { .x = 3.0, .y = -90, .identifier = "B"}, { .x = 0.5, .y = 5000, .identifier = "C" }
        };
        REQUIRE(inputReader.getDynamicPoints() == dynamicPoints);

        REQUIRE(inputReader.getConstraints().empty());
        REQUIRE(inputReader.getGraphics().empty());
    }
}