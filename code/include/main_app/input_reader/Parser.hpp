#pragma once

#include <optional>
#include <filesystem>

#include "main_app/input_reader/LexyComponents.hpp"
#include "main_app/input_reader/Coordinate.hpp"

namespace input_reader::internal::parser {
    class Parser {
      public:
        static std::optional<ast::SimulationState> readFile(const std::filesystem::path &path);
    };
}
