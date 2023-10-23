#pragma once

#include <string>
#include <variant>
#include <vector>
#include <cmath>
#include <memory>
#include <optional>

#include <lexy/action/parse.hpp>
#include <lexy/callback.hpp>
#include <lexy/dsl.hpp>
#include <lexy/input/file.hpp>
#include <lexy/input/string_input.hpp>
#include <lexy_ext/report_error.hpp>

namespace input_reader::internal {
namespace ast {
    using Identifier = std::string;

    using Decimal = double;

    struct Point {
        Identifier identifier;
        Decimal xCoordinate;
        Decimal yCoordinate;
    };

    struct StaticQualifiedPoint {
        Identifier identifier;
    };

    enum ConstraintType {
        FORCE_CONSTRAINT,
        DISTANCE_CONSTRAINT,
    };

    enum ConstraintOperator {
        EQUAL,
        LESS_THAN,
        HIGHER_THAN,
        LESS_OR_EQUAL_THAN,
        HIGHER_OR_EQUAL_THAN,
    };

    struct ConstantConstraint {
        ConstraintOperator constraintOperator;
        Decimal size;
    };

    enum PropertyIdentifier {
        TIME_PROPERTY,
        DISTANCE_PROPERTY
    };

    enum UnaryOperator {
        NEGATIVE,
        SIN, COS, TAN,
        ASIN, ACOS, ATAN,
        SINH, COSH, TANH,
        LN, LOG, EXP, SQRT
    };

    enum BinaryOperator {
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        EXPONENTIAL
    };

    enum Constant {
        TAU, PI
    };

    struct FunctionBody {
        // TODO use variant
        std::optional<std::shared_ptr<FunctionBody>> left;
        std::optional<BinaryOperator> binaryOperator;
        std::optional<std::shared_ptr<FunctionBody>> right;

        std::optional<UnaryOperator> unaryOperator;
        std::optional<std::shared_ptr<FunctionBody>> elem;

        std::optional<std::shared_ptr<FunctionBody>> body;

        std::optional<PropertyIdentifier> identifier;

        std::optional<Decimal> decimal;

        std::optional<Constant> constant;

        FunctionBody(std::shared_ptr<FunctionBody>&& left, BinaryOperator binaryOperator, std::shared_ptr<FunctionBody> right)
          : left(std::move(left))
          , binaryOperator(binaryOperator)
          , right(std::move(right)) {}

        FunctionBody(UnaryOperator unaryOperator, std::shared_ptr<FunctionBody>&& elem)
          : unaryOperator(unaryOperator)
          , elem(std::move(elem)) {}

        explicit FunctionBody(std::shared_ptr<FunctionBody>&& body)
          : body(std::move(body)) {}

        explicit FunctionBody(PropertyIdentifier identifier)
          : identifier(identifier) {}

        explicit FunctionBody(Decimal decimal)
          : decimal(decimal) {}

        explicit FunctionBody(Constant constant)
          : constant(constant) {}

        FunctionBody() = default;
    };

    struct FunctionConstraint {
        FunctionBody body;
    };

    struct Constraint {
        ConstraintType constraintType;
        Identifier pointA;
        Identifier pointB;
        std::variant<ConstantConstraint, FunctionConstraint> constraint;
    };

    struct Bar {
        Identifier pointA;
        Identifier pointB;
    };

    struct Circle {
        Identifier point;
        Decimal radius;
    };

    struct GraphicalStatement {
        std::variant<Circle, Bar> value;
    };

    struct Statement {
        std::variant<Point, StaticQualifiedPoint, Constraint, GraphicalStatement> value;

        template<typename T> explicit Statement(T specificValue) : value(std::move(specificValue)) {}
    };

    using SimulationState = std::vector<Statement>;
} // ast

namespace parser {
    namespace dsl = lexy::dsl;

    constexpr auto staticReserved = LEXY_LIT("static");
    constexpr auto constraintReserved = LEXY_LIT("constraint");
    constexpr auto showReserved = LEXY_LIT("show");

    constexpr auto distanceConstraintReserved = LEXY_LIT("distance");
    constexpr auto forceConstraintReserved = LEXY_LIT("force");

    constexpr auto equalReserved = LEXY_LIT("==");
    constexpr auto lessThanReserved = LEXY_LIT("<");
    constexpr auto higherThanReserved = LEXY_LIT(">");
    constexpr auto lessOrEqualThanReserved = LEXY_LIT("<=");
    constexpr auto higherOrEqualThanReserved = LEXY_LIT(">=");

    constexpr auto sinReserved = LEXY_LIT("sin");
    constexpr auto cosReserved = LEXY_LIT("cos");
    constexpr auto tanReserved = LEXY_LIT("tan");
    constexpr auto asinReserved = LEXY_LIT("asin");
    constexpr auto acosReserved = LEXY_LIT("acos");
    constexpr auto atanReserved = LEXY_LIT("atan");
    constexpr auto sinhReserved = LEXY_LIT("sinh");
    constexpr auto coshReserved = LEXY_LIT("cosh");
    constexpr auto tanhReserved = LEXY_LIT("tanh");
    constexpr auto lnReserved = LEXY_LIT("ln");
    constexpr auto logReserved = LEXY_LIT("log");
    constexpr auto expReserved = LEXY_LIT("exp");
    constexpr auto sqrtReserved = LEXY_LIT("sqrt");

    constexpr auto plusReserved = LEXY_LIT("+");
    constexpr auto minusReserved = LEXY_LIT("-");

    constexpr auto multiplyReserved = LEXY_LIT("*");
    constexpr auto divideReserved = LEXY_LIT("/");

    constexpr auto exponentReserved = LEXY_LIT("^");

    constexpr auto tauReserved = LEXY_LIT("tau");
    constexpr auto piReserved = LEXY_LIT("pi");

    constexpr auto distanceIdentifierReserved = LEXY_LIT("distance");
    constexpr auto distanceShortIdentifierReserved = LEXY_LIT("d");
    constexpr auto timeIdentifierReserved = LEXY_LIT("time");
    constexpr auto timeShortIdentifierReserved = LEXY_LIT("t");

    constexpr auto functionReserved = LEXY_LIT("fun");
    constexpr auto arrowReserved = LEXY_LIT("->");

    constexpr auto barReserved = LEXY_LIT("bar");
    constexpr auto circleReserved = LEXY_LIT("circle");
    constexpr auto radiusReserved = LEXY_LIT("radius");

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
              .map(distanceConstraintReserved, ast::ConstraintType::DISTANCE_CONSTRAINT)
              .map(forceConstraintReserved, ast::ConstraintType::FORCE_CONSTRAINT);

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

    struct Constant {
        struct InvalidConstant {
            static LEXY_CONSTEVAL auto name() { return "constant is not tau or pi"; }
        };

        static constexpr auto types
          = lexy::symbol_table<ast::Constant>
              .map(tauReserved, ast::Constant::TAU)
              .map(piReserved, ast::Constant::PI);

        static constexpr auto rule = [] {
            return dsl::symbol<types> | dsl::error<InvalidConstant>;
        }();
        static constexpr auto value = lexy::construct<ast::Constant>;
    };

    struct PropertyIdentifier {
        struct InvalidPropertyIdentifier {
            static LEXY_CONSTEVAL auto name() { return "property identifier is not time or distance"; }
        };

        static constexpr auto types
          = lexy::symbol_table<ast::PropertyIdentifier>
              .map(timeIdentifierReserved, ast::PropertyIdentifier::TIME_PROPERTY)
              .map(timeShortIdentifierReserved, ast::PropertyIdentifier::TIME_PROPERTY)
              .map(distanceIdentifierReserved, ast::PropertyIdentifier::DISTANCE_PROPERTY)
              .map(distanceShortIdentifierReserved, ast::PropertyIdentifier::DISTANCE_PROPERTY);

        static constexpr auto rule = [] {
            return dsl::symbol<types> | dsl::error<InvalidPropertyIdentifier>;
        }();
        static constexpr auto value = lexy::construct<ast::PropertyIdentifier>;
    };

    struct PropertyIdentifiers {
        static constexpr auto rule = [] {
            auto condition = dsl::peek(dsl::parenthesized.list(dsl::p<PropertyIdentifier>, dsl::sep(dsl::comma)));

            return condition >> (dsl::parenthesized.opt_list(dsl::p<PropertyIdentifier>, dsl::sep(dsl::comma)));
        }();
        static constexpr auto value = lexy::noop;
    };

    struct FunctionBody : lexy::expression_production {
        struct InvalidFunctionBody {
            static LEXY_CONSTEVAL auto name() { return "element is not binary operator, unary operator, parenthesis, identifier, decimal or constant"; }
        };

        static constexpr auto plusOperation = dsl::op(plusReserved);
        static constexpr auto minusOperation = dsl::op(minusReserved);
        static constexpr auto multiplyOperation = dsl::op(multiplyReserved);
        static constexpr auto divideOperation = dsl::op(divideReserved);
        static constexpr auto exponentOperation = dsl::op(exponentReserved);

        static constexpr auto negativeOperation = dsl::op(minusReserved);
        static constexpr auto sinOperation = dsl::op(sinReserved);
        static constexpr auto cosOperation = dsl::op(cosReserved);
        static constexpr auto tanOperation = dsl::op(tanReserved);
        static constexpr auto asinOperation = dsl::op(asinReserved);
        static constexpr auto acosOperation = dsl::op(acosReserved);
        static constexpr auto atanOperation = dsl::op(atanReserved);
        static constexpr auto sinhOperation = dsl::op(sinhReserved);
        static constexpr auto coshOperation = dsl::op(coshReserved);
        static constexpr auto tanhOperation = dsl::op(tanhReserved);
        static constexpr auto lnOperation = dsl::op(lnReserved);
        static constexpr auto logOperation = dsl::op(logReserved);
        static constexpr auto expOperation = dsl::op(expReserved);
        static constexpr auto sqrtOperation = dsl::op(sqrtReserved);

        static constexpr auto atom = [] {
            auto parens = dsl::parenthesized(dsl::recurse<FunctionBody>);
            auto decimal = dsl::peek(dsl::p<Decimal>) >> dsl::p<Decimal>;
            auto constant = dsl::peek(dsl::p<Constant>) >> dsl::p<Constant>;
            auto identifier = dsl::peek(dsl::p<PropertyIdentifier>) >> dsl::p<PropertyIdentifier>;

            return parens | decimal | constant | identifier | dsl::error<InvalidFunctionBody>;
        }();

        struct prefix : dsl::prefix_op {
            static constexpr auto op = negativeOperation
                                       / sinOperation / cosOperation / tanOperation
                                       / asinOperation / acosOperation / atanOperation
                                       / sinhOperation / coshOperation / tanhOperation
                                       / lnOperation / logOperation / expOperation / sqrtOperation;
            using operand = dsl::atom;
        };

        struct exponent : dsl::infix_op_left {
            static constexpr auto op = exponentOperation;
            using operand = prefix;
        };

        struct product : dsl::infix_op_left {
            static constexpr auto op = multiplyOperation / divideOperation;
            using operand = exponent;
        };

        struct sum : dsl::infix_op_left {
            static constexpr auto op = plusOperation / minusOperation;
            using operand = product;
        };

        using operation = sum;

        template<auto Operator, auto Value>
        static constexpr auto parseBinaryOperation = [](const ast::FunctionBody& left, lexy::op<Operator>,
                                                 const ast::FunctionBody& right) {
            return ast::FunctionBody(std::make_shared<ast::FunctionBody>(left), Value,
              std::make_shared<ast::FunctionBody>(right));
        };

        template<auto Operator, auto Value>
        static constexpr auto parseUnaryOperation = [](lexy::op<Operator>, const ast::FunctionBody& operand) {
            return ast::FunctionBody(Value, std::make_shared<ast::FunctionBody>(operand));
        };

        static constexpr auto value = lexy::callback<ast::FunctionBody>(
          parseBinaryOperation<plusOperation, ast::BinaryOperator::PLUS>,
          parseBinaryOperation<minusOperation, ast::BinaryOperator::MINUS>,
          parseBinaryOperation<multiplyOperation, ast::BinaryOperator::TIMES>,
          parseBinaryOperation<divideOperation, ast::BinaryOperator::DIVIDE>,
          parseBinaryOperation<exponentOperation, ast::BinaryOperator::EXPONENTIAL>,
          parseUnaryOperation<negativeOperation, ast::UnaryOperator::NEGATIVE>,
          parseUnaryOperation<sinOperation, ast::UnaryOperator::SIN>,
          parseUnaryOperation<cosOperation, ast::UnaryOperator::COS>,
          parseUnaryOperation<tanOperation, ast::UnaryOperator::TAN>,
          parseUnaryOperation<asinOperation, ast::UnaryOperator::ASIN>,
          parseUnaryOperation<acosOperation, ast::UnaryOperator::ACOS>,
          parseUnaryOperation<atanOperation, ast::UnaryOperator::ATAN>,
          parseUnaryOperation<sinhOperation, ast::UnaryOperator::SINH>,
          parseUnaryOperation<coshOperation, ast::UnaryOperator::COSH>,
          parseUnaryOperation<tanhOperation, ast::UnaryOperator::TANH>,
          parseUnaryOperation<lnOperation, ast::UnaryOperator::LN>,
          parseUnaryOperation<logOperation, ast::UnaryOperator::LOG>,
          parseUnaryOperation<expOperation, ast::UnaryOperator::EXP>,
          parseUnaryOperation<sqrtOperation, ast::UnaryOperator::SQRT>,
          [](const ast::FunctionBody& value) { return ast::FunctionBody(std::make_shared<ast::FunctionBody>(value)); },
          [](ast::PropertyIdentifier identifier) { return ast::FunctionBody(identifier); },
          [](ast::Decimal decimal) { return ast::FunctionBody(decimal); },
          [](ast::Constant constant) { return ast::FunctionBody(constant); }
        );
    };

    struct FunctionConstraint {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(functionReserved
                                       + ws + dsl::p<PropertyIdentifiers>
                                       + ws + arrowReserved);

            auto body = (dsl::member<&ast::FunctionConstraint::body> = dsl::p<FunctionBody>);
            return condition >> (functionReserved + dsl::p<PropertyIdentifiers> + arrowReserved + body);
        }();
        static constexpr auto value = lexy::as_aggregate<ast::FunctionConstraint>;
    };

    struct ConstantConstraint {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(dsl::p<ConstraintOperator> + ws + dsl::p<Decimal>);

            auto constraintOperator = (dsl::member<&ast::ConstantConstraint::constraintOperator> = dsl::p<ConstraintOperator>);
            auto size = (dsl::member<&ast::ConstantConstraint::size> = dsl::p<Decimal>);

            return condition >> (constraintOperator + size);
        }();
        static constexpr auto value = lexy::as_aggregate<ast::ConstantConstraint>;
    };

    struct Constraint {
        struct InvalidConstraint {
            static LEXY_CONSTEVAL auto name() { return "constraint is not constant or function"; }
        };

        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(constraintReserved + ws + dsl::p<ConstraintType> + ws + dsl::p<Identifier>
              + ws + dsl::p<Identifier>);

            auto type = (dsl::member<&ast::Constraint::constraintType> = dsl::p<ConstraintType>);
            auto pointA = (dsl::member<&ast::Constraint::pointA> = dsl::p<Identifier>);
            auto pointB = (dsl::member<&ast::Constraint::pointB> = dsl::p<Identifier>);
            auto constraint = (dsl::member<&ast::Constraint::constraint> = dsl::p<ConstantConstraint>);
            auto function = (dsl::member<&ast::Constraint::constraint> = dsl::p<FunctionConstraint>);

            return condition >> (constraintReserved + type + pointA + pointB + (constraint | function | dsl::error<InvalidConstraint>));
        }();
        static constexpr auto value = lexy::as_aggregate<ast::Constraint>;
    };

    struct Bar {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(barReserved + ws + dsl::p<Identifier> + ws + dsl::p<Identifier>);

            auto pointA = (dsl::member<&ast::Bar::pointA> = dsl::p<Identifier>);
            auto pointB = (dsl::member<&ast::Bar::pointB> = dsl::p<Identifier>);

            return condition >> (barReserved + pointA + pointB);
        }();
        static constexpr auto value = lexy::as_aggregate<ast::Bar>;
    };

    struct Circle {
        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(circleReserved + ws + dsl::p<Identifier> + ws + radiusReserved + ws + dsl::p<Decimal>);

            auto point = (dsl::member<&ast::Circle::point> = dsl::p<Identifier>);
            auto radius = (dsl::member<&ast::Circle::radius> = dsl::p<Decimal>);

            return condition >> (circleReserved + point + radiusReserved + radius);
        }();
        static constexpr auto value = lexy::as_aggregate<ast::Circle>;
    };

    struct GraphicalStatement {
        struct InvalidGraphicalStatement {
            static LEXY_CONSTEVAL auto name() { return "statement is not bar or circle"; }
        };

        static constexpr auto rule = [] {
            auto ws = dsl::whitespace(dsl::ascii::space);
            auto condition = dsl::peek(showReserved + ws);

            auto circle = (dsl::member<&ast::GraphicalStatement::value> = dsl::p<Circle>);
            auto bar = (dsl::member<&ast::GraphicalStatement::value> = dsl::p<Bar>);

            return condition >> (showReserved + (circle | bar | dsl::error<InvalidGraphicalStatement>));
        }();
        static constexpr auto value = lexy::as_aggregate<ast::GraphicalStatement>;
    };

    struct Statement {
        struct InvalidStatement {
            static LEXY_CONSTEVAL auto name() { return "statement is not point, qualifier, constraint or graphical element"; }
        };

        static constexpr auto rule = [] {
            return dsl::p<StaticQualifiedPoint> | dsl::p<Point> | dsl::p<Constraint> | dsl::p<GraphicalStatement> | dsl::error<InvalidStatement>;
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
