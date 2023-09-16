#ifndef CONSTRAINTBASEDSIMULATOR_CONSTRAINTPROPERTY_HPP
#define CONSTRAINTBASEDSIMULATOR_CONSTRAINTPROPERTY_HPP

#include <variant>

namespace input_reader {

using Distance = double;

using ConstraintProperty = std::variant<Distance>;

} // input_reader

#endif// CONSTRAINTBASEDSIMULATOR_CONSTRAINTPROPERTY_HPP
