#ifndef CONSTRAINTBASEDSIMULATOR_STATELOADER_HPP
#define CONSTRAINTBASEDSIMULATOR_STATELOADER_HPP

#include "main_app/input_reader/ReadInput.hpp"

namespace simulator {
class StateLoader {
public:
    static input_reader::ReadInput getLoaded();
};
}

#endif// CONSTRAINTBASEDSIMULATOR_STATELOADER_HPP
