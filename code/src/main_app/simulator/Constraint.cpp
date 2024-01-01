#include "main_app/simulator/Constraint.hpp"

#include <utility>

namespace simulator {
Constraint::Constraint(Constraint::ConstraintFunction constraint, std::vector<std::shared_ptr<Particle>> particles)
    : constraint(std::move(constraint))
    , particles(std::move(particles)) {}

double Constraint::getConstraint(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
  autodiff::VectorXdual accelerationVectors) const {
    autodiff::dual time = 0;
    return constraint(time, positionVectors, velocityVectors, accelerationVectors).val;
}

double Constraint::dConstraint(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
  autodiff::VectorXdual accelerationVectors) const {
    autodiff::dual time = 0;
    const Eigen::VectorXd dC = autodiff::gradient(constraint, autodiff::wrt(time),
      autodiff::at(time, positionVectors, velocityVectors, accelerationVectors));
    return dC.value();
}

Eigen::VectorXd Constraint::jacobian(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
  autodiff::VectorXdual accelerationVectors) const {
    autodiff::dual time = 0;
    const Eigen::VectorXd J = autodiff::gradient(constraint, autodiff::wrt(positionVectors),
      autodiff::at(time, positionVectors, velocityVectors, accelerationVectors));
    return J;
}

Eigen::VectorXd Constraint::d2Jacobian(autodiff::VectorXdual positionVectors, autodiff::VectorXdual velocityVectors,
  autodiff::VectorXdual accelerationVectors) const {
    autodiff::dual time = 0;
    const Eigen::VectorXd dJ = autodiff::gradient(constraint, autodiff::wrt(time, positionVectors),
      autodiff::at(time, positionVectors, velocityVectors, accelerationVectors));
    return dJ;
}

const std::vector<std::shared_ptr<Particle>> &Constraint::getParticles() const {
    return particles;
}

}