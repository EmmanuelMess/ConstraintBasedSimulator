#pragma once

#include "main_app/input_reader/ReadInput.hpp"

namespace simulator {
class StateLoader {
public:
    static input_reader::ReadInput getLoaded();
};
}
