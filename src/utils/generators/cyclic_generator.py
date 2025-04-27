"""
CyclicGenerator

A generator that loops linearly through a defined range, supporting both scalars and tuples.

- If range values are numbers, it interpolates numerically.
- If range values are tuples (e.g., RGB colors), it interpolates each element independently.
- The generator wraps automatically when reaching the end of the range.

Effects can pass 't' externally for synchronized control, or rely on internal stepping for autonomous cycling.

 Example usage:
 gen = CyclicGenerator(range=(0, 100), step=1)
 print(gen.get_value())   # Advances internally
 print(gen.get_value(t=42))  # Or control explicitly with external t
"""

from .base_generator import BaseGenerator

class CyclicGenerator(BaseGenerator):
    """
    A generator that loops linearly through a range, supporting scalars or tuples.
    """
    def __init__(self, range, step, **params):
        super().__init__(range=range, step=step, **params)

    def get_value(self, t=None):
        if t is None:
            t = self.internal_t
            self.internal_t += 1

        start, end = self.range

        if isinstance(start, tuple):
            # Handle tuple interpolation
            result = []
            for s, e in zip(start, end):
                span = e - s
                position = (t * self.step) % span
                normalized = position / span
                result.append(s + span * normalized)
            return tuple(result)
        else:
            # Scalar interpolation
            span = end - start
            position = (t * self.step) % span
            normalized = position / span
            return start + span * normalized
