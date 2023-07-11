#include "main_app/simulation.hpp"

#include <spdlog/spdlog.h>

#include <Eigen/Core>

void simulation::test() {
    Eigen::Matrix3d matrix = Eigen::Matrix3d::Random();
    matrix = (matrix + Eigen::Matrix3d::Constant(1.2)) * 50;

    {
        std::stringstream ss;
        ss << matrix;
        spdlog::info("m = {}", ss.str());
    }

    const Eigen::Vector3d vector(1,2,3);

    {
        std::stringstream ss;
        ss << matrix * vector;
        spdlog::info("m * v = {}", ss.str());
    }
}