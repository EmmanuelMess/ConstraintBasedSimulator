#pragma once

#include <functional>

#include <autodiff/reverse/var.hpp>

#include "Vector2d.hpp"

namespace simulator {
using Constraint = std::function<autodiff::var(autodiff::var positionX, autodiff::var positionY)>;
}
