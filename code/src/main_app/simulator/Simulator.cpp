#include "main_app/simulator/Simulator.hpp"

#include "main_app/grapher/EventManager.hpp"
#include "main_app/simulator/StateLoader.hpp"

namespace simulator {

void Simulator::initialize() {
    const input_reader::ReadInput state = StateLoader::getLoaded();

    particles.reserve(state.getStaticPoints().size() + state.getDynamicPoints().size());
    for (const auto& point : state.getStaticPoints()) {
        particles.push_back({
          .position = Eigen::Vector2f(point.x, point.y),
          .force = Eigen::Vector2f::Zero(),
          .mass = STATIC_POINT_MASS,
        });
    }

    for (const auto& point : state.getDynamicPoints()) {
        particles.push_back({
          .position = Eigen::Vector2f(point.x, point.y),
          .force = Eigen::Vector2f::Zero(),
          .mass = DYNAMIC_POINT_MASS,
        });
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
        particle.force = Eigen::Vector2f::Zero();
    }
}

void Simulator::calculateForces(std::chrono::milliseconds deltaTime) {
    // Function of time constraints go here
}

void Simulator::calculateConstraintForces() {
    // Solve JWJ^T λ = − J̇q̇ − JWQ − k_s C − k_d  Ċ


}

SimulationState Simulator::getCurrentState() const {
    return {};
}

SimulationState Simulator::onRequestState() const {
    return getCurrentState();
}

} // simulator