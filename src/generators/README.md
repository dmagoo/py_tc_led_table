# Generators

This directory contains modular generators that transform `t` (time, step, or input value) into outputs like scalars, colors, or positions.  
Generators are designed to be composable and flexible.

## Design Philosophy
= Generators are pure transformations: they map t (time or step) into outputs.
- Generators do not manage timing, animation loops, or state beyond t.
- Composition is preferred over inheritance to build complex behaviors.
- Effects and apps are responsible for feeding t into generators.

---

## Available Generators

### BaseGenerator
- Abstract base class for all generators.
- Supports `get_value(t)`, `reset()`, and iterator protocol.

### SineGenerator
- Outputs a normalized sine wave (0 to 1) based on `t`.
- Params: `frequency=1.0`, `phase=0.0`

### TweenGenerator
- Linearly interpolates between two values (scalar or tuple) over a duration.
- Params: `range`, `duration`, optional `max_len`

### PingPongGenerator
- Oscillates back and forth between two integer bounds.
- Params: `range_or_range_generator`, optional `step=1`

### CompositeGenerator
- Chains multiple generators together.
- Output of one becomes input to the next.
- Accepts multiple generators via positional arguments.

---

## Example Usage

### Simple Tween

```python
from src.generators.tween_generator import TweenGenerator

gen = TweenGenerator(range=(0, 100), duration=10)
[gen.get_value(t) for t in range(12)]
# Output: [0, 10, 20, ..., 100, 100]
```

---

### Simple PingPong

```python
from src.generators.ping_pong_generator import PingPongGenerator

gen = PingPongGenerator((0, 5))
[gen.get_value(t) for t in range(12)]
# Output: [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1]
```

---

### Chaining Sine → PingPong

```python
from src.generators.sine_generator import SineGenerator
from src.generators.ping_pong_generator import PingPongGenerator

sine_gen = SineGenerator(frequency=0.5)
pingpong_gen = PingPongGenerator((0, 5))

# Scale sine output (0..1) into 0..5 for pingpong
[pingpong_gen.get_value(sine_gen.get_value(t/5) * 5) for t in range(20)]
```

---

### Using CompositeGenerator

```python
from src.generators.composite_generator import CompositeGenerator
from src.generators.sine_generator import SineGenerator
from src.generators.tween_generator import TweenGenerator

sine_gen = SineGenerator(frequency=1.0)
tween_gen = TweenGenerator(range=(0, 255), duration=1)

composite_gen = CompositeGenerator(sine_gen, tween_gen)

[composite_gen.get_value(t/10) for t in range(10)]
# Output: smoothed values between 0 and 255
```

