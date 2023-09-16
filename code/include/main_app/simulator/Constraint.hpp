#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP

#include <functional>


#include "Vector2d.hpp"

namespace simulator {
using Constraint = std::function<double(Vector2d position)>;
}

#endif// CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP
