#ifndef CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
#define CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP

namespace grapher {

class Grapher {
public:
    Grapher();

private:
    bool paused;
    unsigned int speed;

    void onSetSpeed(unsigned int newSpeed);

    void onPause(bool pause);

    void onRefresh();

    void onRequestFrame();
};

} // grapher
#endif// CONSTRAINTBASEDSIMULATOR_GRAPHER_HPP
