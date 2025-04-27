"""
CyclicGenerator

A generator that loops through a range, wrapping around automatically.

- Supports scalar values and tuples (e.g., colors).
- Step controls how fast t progresses across the range.
- Always wraps when reaching the end of the span.

Child of BaseGenerator:
- Implements compute(t) using modular interpolation.

"""
from .base_generator import BaseGenerator

class CyclicGenerator(BaseGenerator):
    """
    A generator that loops linearly through a range, supporting scalars or tuples.
    """
    def __init__(self, range, step=1, **params):
        super().__init__(**params)
        self.range = range
        self.step = step

    def compute(self, t):
        start, end = self.range
        span = end - start if not isinstance(start, tuple) else None

        if isinstance(start, tuple):
            return tuple(self._interp(s, e, t) for s, e in zip(start, end))
        else:
            return self._interp(start, end, t)

    def _interp(self, start, end, t):
        span = end - start
        position = (t * self.step) % span
        normalized = position / span
        return start + span * normalized
