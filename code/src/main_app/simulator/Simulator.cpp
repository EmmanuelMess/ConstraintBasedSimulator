#include "main_app/simulator/Simulator.hpp"

#include <spdlog/spdlog.h>

#include "main_app/GeneralConstants.hpp"
#include "main_app/events_manager/EventManager.hpp"
#include "main_app/simulator/StateLoader.hpp"
#include "main_app/simulator/EigenHelper.hpp"

namespace simulator {

void Simulator::initialize() {
    const input_reader::ReadInput state = StateLoader::getLoaded();

    const std::vector<input_reader::Point>& staticPoints = state.getStaticPoints();
    const std::vector<input_reader::Point>& dynamicPoints = state.getDynamicPoints();

    particles.reserve(staticPoints.size() + dynamicPoints.size());

    std::transform(staticPoints.begin(), staticPoints.end(), std::back_inserter(particles),
      [](const input_reader::Point& point) {
          return std::make_shared<Particle>(point.identifier, Vector2d(point.x, point.y), true);
      });

    std::transform(dynamicPoints.begin(), dynamicPoints.end(), std::back_inserter(particles),
      [](const input_reader::Point& point) {
          return std::make_shared<Particle>(point.identifier, Vector2d(point.x, point.y), false);
      });

    for(const auto& [key, value] : std::unordered_map<input_reader::PointId, input_reader::Constraint> {
           { "B", { input_reader::Constraint::Type::DistanceConstraint, input_reader::Constraint::Constraint::Property(5.0) } }
         }) {
        if(value.constraintType == input_reader::Constraint::Type::DistanceConstraint) {
            const auto constraintFunction = [&value = value](autodiff::dual time, autodiff::VectorXdual position,
                                              autodiff::VectorXdual velocity, autodiff::VectorXdual acceleration) {
                const auto positionFunction = [&position, &velocity, &acceleration](autodiff::dual time) -> autodiff::VectorXdual {
                    return position + time * velocity + (time * time) * 1/2 * acceleration;
                };
                const double distance = std::get<input_reader::Constraint::Distance>(value.properties);
                const autodiff::dual constraint = 0.5 * (positionFunction(time) * positionFunction(time)).sum() - distance;
                return constraint;
            };

            constraints.try_emplace(key, Constraint(constraintFunction, { particles[0], particles[1] }));
        }
    }
}

void Simulator::step() {
    resetForces();
    //TODO add external forces
    calculateConstraintForces();
    // TODO calculate acceleration and apply (for non static functions)

    events_manager::EventManager::getInstance().signalSimulationResult(getCurrentState());
}

void Simulator::resetForces() {
    for (auto &particle : particles) {
        if (particle->isStatic) {
            continue;
        }

        particle->acceleration = Vector2d::Zero();
    }
}

void Simulator::calculateConstraintForces() {
    // Solve JWJ^T λ = − J̇q̇ − JWQ − k_s C − k_d  Ċ
    for(const auto& [id, constraint] : constraints) {
        // TODO compute the vectors for all particles and compute the matrices
        using MatrixDXd = Eigen::Matrix<double, Eigen::Dynamic, constants::DIMENSIONS>;
        MatrixDXd positions(constraint.getParticles().size(), constants::DIMENSIONS);
        MatrixDXd velocities(constraint.getParticles().size(), constants::DIMENSIONS);
        MatrixDXd accelerations(constraint.getParticles().size(), constants::DIMENSIONS);

        for(std::size_t i = 0; i < constraint.getParticles().size(); i++) {
            const std::shared_ptr<Particle>& particle = constraint.getParticles()[i];
            const auto index = static_cast<Eigen::Index>(i);
            positions.row(index) = particle->position.transpose();
            velocities.row(index) = particle->velocity.transpose();
            accelerations.row(index) = particle->acceleration.transpose();
        }

        spdlog::debug("Positions\n{}", internal::EigenHelper::matrixToString(positions.reshaped()));
        spdlog::debug("Velocity\n{}", internal::EigenHelper::matrixToString(velocities.reshaped()));
        spdlog::debug("Accelerations\n{}", internal::EigenHelper::matrixToString(accelerations.reshaped()));

        const double c = constraint.dConstraint(positions.reshaped(), velocities.reshaped(), accelerations.reshaped());
        spdlog::debug("Constraint {}", c);
    }
}

SimulationState Simulator::getCurrentState() const {
    std::vector<SimulationState::ParticlePosition> particlePositions;
    std::transform(particles.begin(), particles.end(), std::back_inserter(particlePositions),
      [](const std::shared_ptr<Particle>& particle){
          return SimulationState::ParticlePosition {
              .x = particle->position[0],
              .y = particle->position[1],
          };
      });

    return {
        .particlePositions = particlePositions,
    };
}

SimulationState Simulator::onRequestState() const {
    return getCurrentState();
}

} // simulator