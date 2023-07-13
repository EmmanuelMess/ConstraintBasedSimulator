#include <catch2/catch_test_macros.hpp>

#include <lexy/action/parse.hpp>
#include <lexy/callback.hpp>
#include <lexy/dsl.hpp>
#include <lexy/input/file.hpp>
#include <lexy_ext/report_error.hpp>
#include <lexy/input/string_input.hpp>

#include <Eigen/Core>

#include <QtCore/QList>

struct Color {
    std::uint8_t r, g, b;
};

namespace grammar {
namespace dsl = lexy::dsl;

struct channel {
    static constexpr auto rule = dsl::integer<std::uint8_t>(dsl::n_digits<2, dsl::hex>);
    static constexpr auto value = lexy::forward<std::uint8_t>;
};

struct color {
    static constexpr auto rule = dsl::hash_sign + dsl::times<3>(dsl::p<channel>);
    static constexpr auto value = lexy::construct<Color>;
};
} // namespace grammar

TEST_CASE("lexy works", "[lexy base]") {
    auto literal = lexy::zstring_input("#FF00FF");
    auto result = lexy::parse<grammar::color>(literal, lexy_ext::report_error);

    REQUIRE(result);
}

TEST_CASE("Eigen works", "[eigen base]") {
    Eigen::Matrix3d matrix = Eigen::Matrix3d::Random();
    matrix = (matrix + Eigen::Matrix3d::Constant(1.2)) * 50;

    const Eigen::Vector3d vector(1,2,3);

    REQUIRE((matrix * vector - Eigen::Vector3d(404.274,512.237,261.153)).sum() <= 0.02);
}

TEST_CASE("Qt6 works", "[qt6 base]") {
    QList<qint8> list;

    list.append(5);

    REQUIRE(list.size() == 1);
}