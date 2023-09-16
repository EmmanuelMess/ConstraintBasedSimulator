#ifndef CONSTRAINTBASEDSIMULATOR_INPUT_READER_CONSTRAINT_HPP
#define CONSTRAINTBASEDSIMULATOR_INPUT_READER_CONSTRAINT_HPP

#include "main_app/input_reader/ConstraintType.hpp"
#include "main_app/input_reader/ConstraintProperty.hpp"

namespace input_reader {

struct Constraint {
    ConstraintType constraintType;
    ConstraintProperty properties;
};

} // input_reader

#endif// CONSTRAINTBASEDSIMULATOR_INPUT_READER_CONSTRAINT_HPP
