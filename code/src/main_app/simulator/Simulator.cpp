#include "main_app/simulator/Simulator.hpp"

#include "main_app/grapher/EventManager.hpp"
#include "main_app/simulator/StateLoader.hpp"

namespace simulator {

void Simulator::initialize() {
    const input_reader::ReadInput state = StateLoader::getLoaded();

    particles.reserve(state.getStaticPoints().size() + state.getDynamicPoints().size());
    for (const auto& point : state.getStaticPoints()) {
        particles.push_back({
          .position = Vector2d(point.x, point.y),
          .force = Vector2d::Zero(),
          .mass = STATIC_POINT_MASS,
        });
    }

    for (const auto& point : state.getDynamicPoints()) {
        particles.push_back({
          .position = Vector2d(point.x, point.y),
          .force = Vector2d::Zero(),
          .mass = DYNAMIC_POINT_MASS,
        });
    }

    for(const auto& [key, value] : state.getConstraints()) {
        if(value.constraintType == input_reader::ConstraintType::DistanceConstraint) {
            constraints[key] = [value](Vector2d position) {
                const double constraint = (0.5 * (position[0] * position[0] + position[1] * position[1]) - 1);
                return constraint - std::get<input_reader::Distance>(value.properties);
            };
        }
    }

    events::EventManager::getInstance().signalRequestState.connect([this] { return onRequestState(); });
}

void Simulator::step(std::chrono::milliseconds deltaTime) {
    resetForces();
    calculateForces(deltaTime);
    calculateConstraintForces();
    // TODO calculate acceleration and apply
}

void Simulator::resetForces() {
    for (auto &particle : particles) {
        particle.force = Vector2d::Zero();
    }
}

void Simulator::calculateForces(std::chrono::milliseconds deltaTime) {
    // Function of time constraints go here
}

void Simulator::calculateConstraintForces() {
    // Solve JWJ^T λ = − J̇q̇ − JWQ − k_s C − k_d  Ċ

    for(const auto& [key, constraintFunction] : constraints) {
        const Particle particle = *std::find_if(particles.begin(), particles.end(), [&key](const Particle& particleB){
            return particleB.identifier == key;
        });

        const double constraint = constraintFunction(particle.position);

    }

}

SimulationState Simulator::getCurrentState() const {
    return {};
}

SimulationState Simulator::onRequestState() const {
    return getCurrentState();
}

} // simulator