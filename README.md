# Constraint Based Simulator

## Input file

```
A = (5.0, 5.0)
B = (7.5.0, 5.0)
C = (10.0, 5.0)
D = (5.0, 10.0)
E = (0.0, 5.0)
F = (5.0, 0.0)

static A
static C
static D
static E
static F

show circle A radius 2.5

constraint distance A B == 2.5

constraint force C B fun (t) -> sin(tau/4   + tau * 0.5 * t)
constraint force F B fun (t) -> sin(0       + tau * 0.5 * t)
constraint force E B fun (t) -> sin(tau*3/4 + tau * 0.5 * t)
constraint force D B fun (t) -> sin(tau/2   + tau * 0.5 * t)
```

## Sample

<img src="./design/diagrams/sample-diagram.png"/>

## Architecture

<img src="./design/diagrams/component/high level components.png"/>

## Thanks

- [An Introduction to Physically Based Modeling: Constrained Dynamics](https://www.cs.cmu.edu/~baraff/pbm/constraints.pdf)
- [Lexy parser](https://github.com/foonathan/lexy)