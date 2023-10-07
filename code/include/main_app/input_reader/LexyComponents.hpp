#pragma once

#include <string>
#include <variant>
#include <vector>
#include <cmath>

#include <lexy/action/parse.hpp>
#include <lexy/callback.hpp>
#include <lexy/dsl.hpp>
#include <lexy/input/file.hpp>
#include <lexy/input/string_input.hpp>
#include <lexy_ext/report_error.hpp>

#include "main_app/input_reader/Coordinate.hpp"

namespace input_reader::internal {
namespace ast {
    using Identifier = std::string;

    using Decimal = Coordinate;

    struct Point {
        Identifier identifier;
        Decimal xCoordinate;
        Decimal yCoordinate;
    };

    struct StaticQualifiedPoint {
        Identifier identifier;
    };

    enum ConstraintType {
        FORCE,
        DISTANCE,
    };

    enum ConstraintOperator {
        EQUAL,
        LESS_THAN,
        HIGHER_THAN,
        LESS_OR_EQUAL_THAN,
        HIGHER_OR_EQUAL_THAN,
    };

    struct Constraint {
        ConstraintType constraintType;
        Identifier pointA;
        Identifier pointB;
        ConstraintOperator constraintOperator;
        Decimal size;
    };

    struct Statement {
        std::variant<Point, StaticQualifiedPoint, Constraint> value;

        template<typename T> explicit Statement(T specificValue) : value(std::move(specificValue)) {}
    };

    using SimulationState = std::vector<Statement>;
} // ast

    namespace parser {
    namespace dsl = lexy::dsl;

    constexpr auto staticReserved = LEXY_LIT("static");
    constexpr auto constraintReserved = LEXY_LIT("constraint");

    constexpr auto distanceReserved = LEXY_LIT("distance");
    constexpr auto forceReserved = LEXY_LIT("force");

    constexpr auto equalReserved = LEXY_LIT("==");
    constexpr auto lessThanReserved = LEXY_LIT("<");
    constexpr auto higherThanReserved = LEXY_LIT(">");
    constexpr auto lessOrEqualThanReserved = LEXY_LIT("<=");
    constexpr auto higherOrEqualThanReserved = LEXY_LIT(">=");

    struct Identifier : lexy::token_production {
        static constexpr auto rule = [] {
            auto head = dsl::ascii::alpha_underscore;
            auto tail = dsl::ascii::alpha_digit_underscore;
            return dsl::identifier(head, tail).reserve(staticReserved);
        }();

        static constexpr auto value = lexy::as_string<ast::Identifier, lexy::utf8_encoding>;
    };

    struct Decimal : lexy::token_production {
        struct IntegerPart : lexy::transparent_production {
            static constexpr auto rule = dsl::minus_sign + dsl::integer<int>(dsl::digits<>.no_leading_zero());
            static constexpr auto value = lexy::as_integer<int>;
        };

        struct DecimalPart : lexy::transparent_production {
            static constexpr auto rule = dsl::lit_c<'.'> >> dsl::integer<int>(dsl::digits<>);
            static constexpr auto value = lexy::as_integer<int>;
        };

        static constexpr auto rule = dsl::peek(dsl::lit_c<'-'> / dsl::digit<>)
                                     >> (dsl::p<IntegerPart> + dsl::opt(dsl::p<DecimalPart>));
        static constexpr auto value = lexy::callback<ast::Decimal>([](int integer, lexy::nullopt) { return integer; },
          [](auto integer, int decimal) {
              const double numberOfDigits = decimal > 0 ? std::ceil(std::log10(decimal)) : 1;

              return static_cast<double>(integer) + decimal * std::pow(10.0, -1 * numberOfDigits);
          });
    };

    struct Point {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(dsl::p<Identifier> + ws + dsl::equal_sign + ws
                                       + dsl::parenthesized(dsl::p<Decimal> + ws + dsl::comma + ws + dsl::p<Decimal>));

            auto identifier = (dsl::member<&ast::Point::identifier> = dsl::p<Identifier>);

            auto xCoordinate = (dsl::member<&ast::Point::xCoordinate> = dsl::p<Decimal>);
            auto yCoordinate = (dsl::member<&ast::Point::yCoordinate> = dsl::p<Decimal>);

            return condition
                   >> (identifier + dsl::equal_sign + dsl::parenthesized(xCoordinate + dsl::comma + yCoordinate));
        }();

        static constexpr auto value = lexy::as_aggregate<ast::Point>;
    };

    struct StaticQualifiedPoint {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(staticReserved + ws + dsl::p<Identifier>);

            auto identifier = (dsl::member<&ast::StaticQualifiedPoint::identifier> = dsl::p<Identifier>);

            return condition >> (staticReserved + identifier);
        }();

        static constexpr auto value = lexy::as_aggregate<ast::StaticQualifiedPoint>;
    };

    struct ConstraintType {
        struct InvalidConstraintType {
            static LEXY_CONSTEVAL auto name() { return "constraint is not force or distance"; }
        };

        static constexpr auto types
          = lexy::symbol_table<ast::ConstraintType>
              .map(distanceReserved, ast::ConstraintType::DISTANCE)
              .map(forceReserved, ast::ConstraintType::FORCE);

        static constexpr auto rule = [] {
            return dsl::symbol<types> | dsl::error<InvalidConstraintType>;
        }();
        static constexpr auto value = lexy::construct<ast::ConstraintType>;
    };

    struct ConstraintOperator {
        struct InvalidConstraintOperator {
            static LEXY_CONSTEVAL auto name() { return "constraint operator is not ==, <, >, <= or >="; }
        };

        static constexpr auto types
          = lexy::symbol_table<ast::ConstraintOperator>
              .map(equalReserved, ast::ConstraintOperator::EQUAL)
              .map(lessThanReserved, ast::ConstraintOperator::LESS_THAN)
              .map(higherThanReserved, ast::ConstraintOperator::HIGHER_THAN)
              .map(lessOrEqualThanReserved, ast::ConstraintOperator::LESS_OR_EQUAL_THAN)
              .map(higherOrEqualThanReserved, ast::ConstraintOperator::HIGHER_OR_EQUAL_THAN);

        static constexpr auto rule = [] {
            return dsl::symbol<types> | dsl::error<InvalidConstraintOperator>;
        }();
        static constexpr auto value = lexy::construct<ast::ConstraintOperator>;
    };

    struct Constraint {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(constraintReserved + ws + dsl::p<ConstraintType> + ws + dsl::p<Identifier>
              + ws + dsl::p<Identifier> + ws + dsl::p<ConstraintOperator> + ws + dsl::p<Decimal>);

            auto type = (dsl::member<&ast::Constraint::constraintType> = dsl::p<ConstraintType>);
            auto pointA = (dsl::member<&ast::Constraint::pointA> = dsl::p<Identifier>);
            auto pointB = (dsl::member<&ast::Constraint::pointB> = dsl::p<Identifier>);
            auto constraintOperator = (dsl::member<&ast::Constraint::constraintOperator> = dsl::p<ConstraintOperator>);
            auto size = (dsl::member<&ast::Constraint::size> = dsl::p<Decimal>);

            return condition >> (constraintReserved + type + pointA + pointB + constraintOperator + size);
        }();
        static constexpr auto value = lexy::as_aggregate<ast::Constraint>;
    };

    struct Statement {
        struct InvalidStatement {
            static LEXY_CONSTEVAL auto name() { return "statement is not point, qualifier, constraint or graphical element"; }
        };

        static constexpr auto rule = [] {
            return dsl::p<StaticQualifiedPoint> | dsl::p<Point> | dsl::p<Constraint> | dsl::error<InvalidStatement>;
        }();
        static constexpr auto value = lexy::construct<ast::Statement>;
    };

    /**
         * Entrypoint
     */
    struct SimulationState {
        static constexpr auto whitespace = dsl::ascii::blank / dsl::ascii::newline;

        static constexpr auto rule = dsl::terminator(dsl::eof).opt_list(dsl::p<Statement>);
        static constexpr auto value = lexy::as_list<ast::SimulationState>;
    };
} // parser
}
