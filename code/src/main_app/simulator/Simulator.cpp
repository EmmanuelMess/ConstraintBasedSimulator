#include "main_app/simulator/Simulator.hpp"

#include <spdlog/spdlog.h>

#include "main_app/grapher/EventManager.hpp"
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
           { "B", { input_reader::ConstraintType::DistanceConstraint, input_reader::ConstraintProperty(5.0) } }
         }) {
        if(value.constraintType == input_reader::ConstraintType::DistanceConstraint) {
            constraints[key] = [value](const autodiff::var& positionX, const autodiff::var& positionY) {
                const autodiff::var constraint = (0.5 * (positionX * positionX + positionY * positionY) - 1);
                return constraint - std::get<input_reader::Distance>(value.properties);
            };
        }
    }

    events::EventManager::getInstance().signalRequestState.connect([this] { return onRequestState(); });
}

void Simulator::step() {
    resetForces();
    //TODO calculateForces(deltaTime);
    calculateConstraintForces();
    // TODO calculate acceleration and apply
}

void Simulator::resetForces() {
    for (auto &particle : particles) {
        particle.force = Vector2d::Zero();
    }
}

void Simulator::calculateConstraintForces() {
    // Solve JWJ^T λ = − J̇q̇ − JWQ − k_s C − k_d  Ċ

    for(const auto& [key, constraintFunction] : constraints) {
        const Particle particle = *std::find_if(particles.begin(), particles.end(), [&key](const Particle& particleB){
            return particleB.identifier == key;
        });

        autodiff::var x = particle.position[0];
        autodiff::var y = particle.position[1];

        autodiff::var constraint = constraintFunction(x, y);
        auto constraint1st = autodiff::derivatives(constraint, autodiff::wrt(x));

        spdlog::info("Particle ({}, {}): Compute constraint {}", particle.position[0], particle.position[1], static_cast<double>(constraint));
        spdlog::info("Particle ({}, {}): Compute constraint {}", particle.position[0], particle.position[1], constraint1st[0]);
    }

}

SimulationState Simulator::getCurrentState() const {
    return {
        .particles = particles,
        .constraints = constraints,
    };
}

SimulationState Simulator::onRequestState() const {
    return getCurrentState();
}

} // simulator