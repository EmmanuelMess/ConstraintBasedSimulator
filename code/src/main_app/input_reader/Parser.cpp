#include "main_app/input_reader/Parser.hpp"

std::optional<input_reader::internal::ast::SimulationState> input_reader::internal::parser::Parser::readFile(const std::filesystem::path& path) {
    const auto input = lexy::read_file<lexy::utf8_encoding>(path.c_str());
    const auto result = lexy::parse<internal::parser::SimulationState>(input.buffer(), lexy_ext::report_error.path(path.c_str()));

    if (!result.has_value()) {
        return { };
    }

    return { result.value() };
}