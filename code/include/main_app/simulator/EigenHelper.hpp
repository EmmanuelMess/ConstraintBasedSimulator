#pragma once

#include <string>

#include <sstream>

namespace simulator::internal {
class EigenHelper {
public:
    template<class Matrix>
    static std::string matrixToString(const Matrix& matrix) {
        // TODO actually use an Eigen function for this
        std::stringstream ss;
        ss << matrix;
        return ss.str();
    }
};
}