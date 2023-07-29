#include <catch2/catch_test_macros.hpp>

#include <Eigen/Core>

TEST_CASE("Eigen works", "[eigen base]") {
    const Eigen::Matrix3d matrix = Eigen::Matrix3d::Random();
    const Eigen::Matrix3d constant = Eigen::Matrix3d::Constant(1.2);
    const int constantScalar = 50;

    const Eigen::Matrix3d matrix1 = (matrix + constant) * constantScalar;

    const Eigen::Vector3d vector(1,2,3);
    const Eigen::Vector3d result(404.274,512.237,261.153);
    const double margin = 0.02;

    REQUIRE((matrix1 * vector - result).sum() <= margin);
}

