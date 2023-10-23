#pragma once

#include <variant>

namespace input_reader {

struct Constraint {
    enum Type {
        DistanceConstraint,
        ForceConstraint
    };

    using Distance = double;
    using Property = std::variant<Distance>;

    Type constraintType;
    Property properties;
};

} // input_reader
