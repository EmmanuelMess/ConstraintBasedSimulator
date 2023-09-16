#include <string>

#include "main_app/input_reader/Coordinate.hpp"
#include "main_app/input_reader/PointId.hpp"

namespace input_reader {

struct Point {
    Coordinate x;
    Coordinate y;

    /**
     * Unique name of this point, defined in the state initialization file
     */
    PointId identifier;

    auto operator<=>(const Point&) const = default; // TODO check if only comparing name is better
};

} // input_reader

namespace std {
template<> struct hash<input_reader::Point> {
    std::size_t operator()(input_reader::Point const &point) const noexcept { return std::hash<input_reader::PointId>{}(point.identifier); }
};
} // std