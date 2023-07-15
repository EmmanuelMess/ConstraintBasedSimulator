# Constraint Based Simulator

## Requirements

Read a file that contains the initial simulation state and constraints.

Show the simulation to the user in a window:
* The window should have play, pause, play speed controls  that set the simulation speed.
* Two simulation points can have between them, a (visual only):
  * bar
  * coil
* One simulation point can have a visual only circle around it.

The simulation consists of a set of static points that are anchored to a set of dynamic points by
constraints:

* Distance constraints:
  * ==, <, >, <=, >=
* Force constraints:
  * Constant force towards point
  * Constant force away from point
  * constant plus sin(x) force from point

## Items that could change (as a probability)

### High

* File format
* UI

### Medium



### Low

* The simulation algorithms