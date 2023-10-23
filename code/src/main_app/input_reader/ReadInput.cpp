#include "main_app/input_reader/ReadInput.hpp"

#include <algorithm>
#include <ranges>
#include <set>

#include <spdlog/spdlog.h>

#include "main_app/input_reader/Parser.hpp"
#include "main_app/util/VariadicOverload.hpp"

namespace input_reader {
bool ReadInput::readFile(const std::filesystem::path &path) {
    spdlog::info("Loading simulation file {}", path.string());

    staticPoints.clear();
    dynamicPoints.clear();
    constraints.clear();
    graphics.clear();

    const auto statementsOptional = internal::parser::Parser::readFile(path);

    if (!statementsOptional) {
        spdlog::error("Parsing error! ");
        return false;
    }

    const auto &statements = *statementsOptional;

    std::vector<internal::ast::Point> points;
    std::set<std::string> identifiersForStaticPoints;

    for (const auto &statement : statements) {
        std::visit(VariadicOverload {
          [&points](const internal::ast::Point& point){
              points.emplace_back(point);
          },
          [&identifiersForStaticPoints](const internal::ast::StaticQualifiedPoint& qualifier){
              identifiersForStaticPoints.emplace(qualifier.identifier);
          },
          [this](const internal::ast::Constraint& constraint) {
              constraints[constraint.pointA] = { };
              constraints[constraint.pointB] = { };
          },
          [this](const internal::ast::GraphicalStatement& graphicalStatement){
              std::visit(VariadicOverload {
                  [this](const internal::ast::Bar& bar){
                      graphics[bar.pointA] = { };
                      graphics[bar.pointB] = { };
                  },
                  [this](const internal::ast::Circle& circle){
                      graphics[circle.point] = { };
                  },
              }, graphicalStatement.value);
          },
        }, statement.value);
    }

    {
        staticPoints.reserve(identifiersForStaticPoints.size());
        dynamicPoints.reserve(points.size() - identifiersForStaticPoints.size());

        for (const auto &point : points) {
            const bool isStatic = identifiersForStaticPoints.contains(point.identifier);
            if (isStatic) {
                staticPoints.emplace_back(Point{
                  .x = point.xCoordinate,
                  .y = point.yCoordinate,
                  .identifier = point.identifier,
                });
            } else {
                dynamicPoints.emplace_back(Point{
                  .x = point.xCoordinate,
                  .y = point.yCoordinate,
                  .identifier = point.identifier,
                });
            }
        }
    }

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