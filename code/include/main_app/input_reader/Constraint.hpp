#pragma once

#include "main_app/input_reader/ConstraintType.hpp"
#include "main_app/input_reader/ConstraintProperty.hpp"

namespace input_reader {

struct Constraint {
    ConstraintType constraintType;
    ConstraintProperty properties;
};

} // input_reader
