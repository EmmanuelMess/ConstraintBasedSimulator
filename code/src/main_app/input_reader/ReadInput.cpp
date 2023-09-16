#include "main_app/input_reader/ReadInput.hpp"

#include <algorithm>
#include <ranges>
#include <set>

#include <spdlog/spdlog.h>

#include "main_app/input_reader/Parser.hpp"

namespace input_reader {
bool ReadInput::readFile(const std::filesystem::path &path) {
    const auto statementsOptional = internal::parser::Parser::readFile(path);

    if (!statementsOptional) {
        spdlog::error("Parsing error! ");
        return false;
    }

    const auto &statements = *statementsOptional;

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

        for (const auto &point : points) {
            const bool isStatic = identifiersForStaticPoints.contains(point.identifier);
            if (!isStatic) { continue; }

            staticPoints.emplace_back(Point{
              .x = point.xCoordinate,
              .y = point.yCoordinate,
              .identifier = point.identifier,
            });
        }
    }


    {
        dynamicPoints.clear();
        dynamicPoints.reserve(points.size() - identifiersForStaticPoints.size());
        for (const auto &point : points) {
            const auto isStatic = identifiersForStaticPoints.contains(point.identifier);
            if (isStatic) { continue; }

            dynamicPoints.emplace_back(Point{
              .x = point.xCoordinate,
              .y = point.yCoordinate,
              .identifier = point.identifier,
            });
        }
    }

    constraints = {};
    graphics = {};

    return true;
}

std::vector<Point> ReadInput::getStaticPoints() const { return staticPoints; }

std::vector<Point> ReadInput::getDynamicPoints() const { return dynamicPoints; }

std::unordered_map<PointId, Constraint> ReadInput::getConstraints() const {
    return constraints;
}

std::unordered_map<PointId, GraphicalElement> ReadInput::getGraphics() const {
    return graphics;
}
}