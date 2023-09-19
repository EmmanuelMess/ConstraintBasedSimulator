#pragma once

#include <filesystem>
#include <vector>
#include <unordered_map>

#include "main_app/input_reader/Constraint.hpp"
#include "main_app/input_reader/GraphicalElement.hpp"
#include "main_app/input_reader/Point.hpp"

namespace input_reader {

class ReadInput {
public:
    [[nodiscard]] bool readFile(const std::filesystem::path& path);

    std::vector<Point> getStaticPoints() const;
    std::vector<Point> getDynamicPoints() const;
    std::unordered_map<PointId, Constraint> getConstraints() const;
    std::unordered_map<PointId, GraphicalElement> getGraphics() const;

private:
    std::vector<Point> staticPoints;
    std::vector<Point> dynamicPoints;
    std::unordered_map<PointId, Constraint> constraints;
    std::unordered_map<PointId, GraphicalElement> graphics;
};

} // input_reader
