#ifndef CONSTRAINTBASEDSIMULATOR_SEMANTICSCHECK_HPP
#define CONSTRAINTBASEDSIMULATOR_SEMANTICSCHECK_HPP

#include "main_app/input_reader/LexyComponents.hpp"

namespace input_reader::internal::semantics {
class SemanticsCheck {
    static bool checkSemantics(parser::SimulationState);
};
}

#endif// CONSTRAINTBASEDSIMULATOR_SEMANTICSCHECK_HPP
