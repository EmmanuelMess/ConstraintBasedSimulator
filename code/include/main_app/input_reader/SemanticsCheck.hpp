#pragma once

#include "main_app/input_reader/LexyComponents.hpp"

namespace input_reader::internal::semantics {
class SemanticsCheck {
    static bool checkSemantics(const ast::SimulationState& simulationState);
};
}
