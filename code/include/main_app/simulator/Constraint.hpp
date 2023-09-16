#ifndef CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP
#define CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP

#include <functional>

#include <autodiff/reverse/var.hpp>

#include "Vector2d.hpp"

namespace simulator {
using Constraint = std::function<autodiff::var(autodiff::var positionX, autodiff::var positionY)>;
}
#endif// CONSTRAINTBASEDSIMULATOR_SIMULATOR_CONSTRAINT_HPP
