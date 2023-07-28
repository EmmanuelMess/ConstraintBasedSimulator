#include "main_app/input_reader/ReadInput.hpp"

#include <algorithm>
#include <ranges>
#include <set>

#include <spdlog/spdlog.h>

bool input_reader::ReadInput::readFile(const std::filesystem::path& path) {
    auto input = lexy::read_file<lexy::utf8_encoding>(path.c_str());
    auto result = lexy::parse<internal::grammar::SimulationState>(input.buffer(), lexy_ext::report_error.path(path.c_str()));

    if (!result.has_value()) {
        spdlog::error("Parsing error! ");
        return false;
    }

    const auto statements = result.value();
    spdlog::info(std::get<internal::ast::Point>(statements.at(0).value).identifier);

    const auto [points, identifiersForStaticPoints] = [&statements]() {
        std::vector<internal::ast::Point> pointsInternal;
        std::set<std::string> identifiersForStaticPointsInternal;

        for (const auto &statement : statements) {
            if (std::holds_alternative<internal::ast::Point>(statement.value)) {
                const auto point = std::get<internal::ast::Point>(statement.value);
                pointsInternal.emplace_back(point);
            } else if (std::holds_alternative<internal::ast::StaticQualifiedPoint>(statement.value)) {
                const auto qualifier = std::get<internal::ast::StaticQualifiedPoint>(statement.value);
                const auto qualifiedIdentifier = qualifier.identifier;
                identifiersForStaticPointsInternal.emplace(qualifiedIdentifier);
            }
        }

        return std::pair(pointsInternal, identifiersForStaticPointsInternal);
    }();

    {
        staticPoints.clear();
        staticPoints.reserve(identifiersForStaticPoints.size());

        for (const auto& point : points) {
            const bool isStatic = identifiersForStaticPoints.contains(point.identifier);
            if (!isStatic) { continue; }

            staticPoints.emplace_back(Point {
              .x = point.xCoordinate,
              .y = point.yCoordinate,
              .name = point.identifier,
            });
        }
    }


    {
        dynamicPoints.clear();
        dynamicPoints.reserve(points.size() - identifiersForStaticPoints.size());
        for (const auto& point : points) {
            const auto isStatic = identifiersForStaticPoints.contains(point.identifier);
            if (isStatic) { continue; }

            dynamicPoints.emplace_back(Point {
              .x = point.xCoordinate,
              .y = point.yCoordinate,
              .name = point.identifier,
            });
        }
    }

    constraints = {};
    graphics = {};

    return true;
}

std::vector<input_reader::Point> input_reader::ReadInput::getStaticPoints() const {
    return staticPoints;
}

std::vector<input_reader::Point> input_reader::ReadInput::getDynamicPoints() const {
    return dynamicPoints;
}

std::unordered_map<input_reader::Point, input_reader::Constraint> input_reader::ReadInput::getConstraints() const {
    return constraints;
}

std::unordered_map<input_reader::Point, input_reader::GraphicalElement> input_reader::ReadInput::getGraphics() const {
    return graphics;
}