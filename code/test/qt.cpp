#include <catch2/catch_test_macros.hpp>

#include <QtCore/QList>

TEST_CASE("Qt6 works", "[qt6 base]") {
    QList<qint8> list;

    const quint8 constant = 5;

    list.append(constant);

    REQUIRE(list.size() == 1);
}