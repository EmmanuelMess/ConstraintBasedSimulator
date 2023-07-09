# Simulation file definition

## Point

Defines a point.

```
<name> = (<float>, <float>)
```

#### Example:

```
A = (1.0, 1.0)
```

## Static element

Sets an object as not affected by simulation. This object maintains its position in space during the simulation.

```
static <name>
```

#### Example:

```
A = (1.0, 1.0)
static A
```

## Constraint

### Distance constraint

```
constraint distance <name> <name> <type> <float>
```

#### Examples:

```
A = (0.0, 0.0)
B = (0.0, 5.0)
static A
constraint distance A B == 5.0
```

```
A = (0.0, 0.0)
B = (0.0, 5.0)
static A
constraint distance A B < 5.0
```

### Force constraint

```
constraint force <name> <name> <type> <float>
```

```
A = (0.0, 0.0)
B = (0.0, 5.0)
static A
constraint force A B fun (dist) -> 0.05 * 1 / (dist ^ 2)
```

## Graphical

### Bar

Show a bar between points

```
show bar <name> <name>
```

#### Example:

```
A = (0.0, 0.0)
B = (0.0, 5.0)
static A
constraint distance A B == 5.0
show bar A B
```

### Circle

Show a circle with center in a point

```
show circle <name> radius <float>
```

#### Example:

```
A = (0.0, 0.0)
B = (0.0, 5.0)
static A
constraint distance A B >= 5.0
show circle A radius 5.0
```

