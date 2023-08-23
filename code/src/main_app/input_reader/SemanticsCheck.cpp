#include "main_app/input_reader/SemanticsCheck.hpp"

namespace input_reader::internal::semantics {
bool SemanticsCheck::checkSemantics(const ast::SimulationState& simulationState) {
    return !simulationState.empty();
}
}