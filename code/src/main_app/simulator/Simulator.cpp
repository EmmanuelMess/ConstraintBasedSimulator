#include "main_app/simulator/Simulator.hpp"

#include <spdlog/spdlog.h>

#include "main_app/events_manager/EventManager.hpp"
#include "main_app/simulator/StateLoader.hpp"

namespace simulator {

void Simulator::initialize() {
    const input_reader::ReadInput state = StateLoader::getLoaded();

    const std::vector<input_reader::Point>& staticPoints = state.getStaticPoints();
    const std::vector<input_reader::Point>& dynamicPoints = state.getDynamicPoints();

    particles.reserve(staticPoints.size() + dynamicPoints.size());

    std::transform(staticPoints.begin(), staticPoints.end(), std::back_inserter(particles),
      [](const input_reader::Point& point){
        return Particle {
            Vector2d(point.x, point.y),
            Vector2d::Zero(),
            STATIC_POINT_MASS,
            point.identifier
        };
    });

    std::transform(dynamicPoints.begin(), dynamicPoints.end(), std::back_inserter(particles),
    [](const input_reader::Point& point){
        return Particle {
            Vector2d(point.x, point.y),
            Vector2d::Zero(),
            DYNAMIC_POINT_MASS,
            point.identifier
        };
    });

    for(const auto& [key, value] : std::unordered_map<input_reader::PointId, input_reader::Constraint> {
           { "B", { input_reader::Constraint::Type::DistanceConstraint, input_reader::Constraint::Constraint::Property(5.0) } }
         }) {
        if(value.constraintType == input_reader::Constraint::Type::DistanceConstraint) {
            constraints[key] = [&value = value](const autodiff::var& positionX, const autodiff::var& positionY) {
                const autodiff::var constraint = (0.5 * (positionX * positionX + positionY * positionY) - 1);
                return constraint - std::get<input_reader::Constraint::Distance>(value.properties);
            };
        }
    }
}

void Simulator::step() {
    resetForces();
    //TODO calculateForces(deltaTime);
    calculateConstraintForces();
    // TODO calculate acceleration and apply

    events_manager::EventManager::getInstance().signalSimulationResult(getCurrentState());
}

void Simulator::resetForces() {
    for (auto &particle : particles) {
        particle.force = Vector2d::Zero();
    }
}

void Simulator::calculateConstraintForces() {
    // Solve JWJ^T λ = − J̇q̇ − JWQ − k_s C − k_d  Ċ

    for(const auto& constraint : constraints) {
        const std::string& key = constraint.first;
        const Constraint& constraintFunction = constraint.second;

        const Particle particle = *std::find_if(particles.begin(), particles.end(), [&key](const Particle& particleB){
            return particleB.identifier.size() == key.size();
        });

        autodiff::var x = particle.position[0];
        const autodiff::var y = particle.position[1];

        const autodiff::var constraintF = constraintFunction(x, y);
        auto constraint1st = autodiff::derivatives(constraintF, autodiff::wrt(x));

        spdlog::info("Particle ({}, {}): Compute constraint {}", particle.position[0], particle.position[1], static_cast<double>(constraintF));
        spdlog::info("Particle ({}, {}): Compute constraint {}", particle.position[0], particle.position[1], constraint1st[0]);
    }

}

SimulationState Simulator::getCurrentState() const {
    std::vector<SimulationState::ParticlePosition> particlePositions;
    std::transform(particles.begin(), particles.end(), std::back_inserter(particlePositions),
      [](const Particle& particle){
          return SimulationState::ParticlePosition {
              .x = particle.position[0],
              .y = particle.position[1],
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