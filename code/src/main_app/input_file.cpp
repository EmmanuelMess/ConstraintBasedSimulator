#include "main_app/input_file.hpp"

#include <spdlog/spdlog.h>

int input_reader::test() {
    /*
    const auto *const path = "example1.state";
    auto input = lexy::read_file(path);
    auto result = lexy::parse<grammar::color>(input.buffer(), lexy_ext::report_error.path(path));
    if (result.has_value()) {
        auto color = result.value();
        spdlog::info("#{}{}{}", color.r, color.g, color.b);
    }
     */
    auto literal = lexy::zstring_input("#FF00FF");
    auto result = lexy::parse<grammar::color>(literal, lexy_ext::report_error);
    if (result.has_value()) {
        auto color = result.value();
        spdlog::info("#{} {} {}", color.r, color.g, color.b);
    }

    return result ? 0 : 1;
}