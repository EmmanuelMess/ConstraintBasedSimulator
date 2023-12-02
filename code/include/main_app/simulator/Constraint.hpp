#pragma once

#include <memory>
#include <vector>
#include <functional>

#include <autodiff/forward/dual.hpp>
#include <autodiff/forward/dual/eigen.hpp>

#include "Vector2d.hpp"
#include "Particle.hpp"

namespace simulator {
class Constraint {
public:
    using ConstraintFunction = std::function<autodiff::dual(autodiff::dual time, autodiff::VectorXdual positionVectors,
      autodiff::VectorXdual velocityVectors, autodiff::VectorXdual accelerationVectors)>;

    Constraint(ConstraintFunction constraint, std::vector<std::shared_ptr<Particle>> particles);

    [[nodiscard]] double dConstraint(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
      autodiff::VectorXdual accelerationVectors) const;

    [[nodiscard]] Eigen::VectorXd jacobian(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
      autodiff::VectorXdual accelerationVectors) const;
    [[nodiscard]] Eigen::VectorXd d2Jacobian(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
      autodiff::VectorXdual accelerationVectors) const;

    [[nodiscard]] const std::vector<std::shared_ptr<Particle>> &getParticles() const;

private:
    Constraint::ConstraintFunction constraint;
    std::vector<std::shared_ptr<Particle>> particles;
};
}